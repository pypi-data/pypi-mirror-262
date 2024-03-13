"""
Top level API for scoring existing matches

"""

import pandas as pd
import numpy as np
import csv
import os

import traceback

from flap.database.sql import SqlDB
from flap.matcher.sql_matcher import SqlMatcher
from flap.database.sql_in_memory import SqlDBInMemory
from flap.parser.rule_parser_fast import RuleParserFast
from flap.utils import join_uprn_fields, available_cpu_count


def csv_row_counter(filename):

    with open(filename, 'r') as f:
        row_count = sum(1 for _ in csv.reader(f))

    return row_count


def read_csv_header(filename):

    with open(filename, 'r') as f:
        dict_reader = csv.DictReader(f)
        headers = dict_reader.fieldnames

    return headers


def _load_all_csv_from_path(path, **kwargs):
    csv_files = [os.path.join(path, p) for p in os.listdir(path) if '.csv' in p]

    index_exists = _check_index(csv_files[0])

    if index_exists:
        dfs = [pd.read_csv(p, index_col=0, **kwargs) for p in csv_files]
    else:
        dfs = [pd.read_csv(p, **kwargs) for p in csv_files]

    return pd.concat(dfs)


def _check_index(csv_file):
    with open(csv_file, 'r') as f:
        header_0 = f.readline().split(',')[0]

    return header_0 == ''


def generate_chunks_of_dataframe(df, chunk_size):

    i = 0

    while (i + chunk_size) < len(df):

        yield df.iloc[i:(i + chunk_size)]

        i += chunk_size

    yield df.iloc[i:]


def score(input_csv, db_path, output_file_path=None, raw_output_path=None,
          in_progress_log_path=None, max_log_interval=4800,
          batch_size=10000, max_workers=None, in_memory_db=False, classifier_model_path=None,
          input_address_col='input_address', uprn_col='uprn'):

    """
    This is the top level function for scoring existing matches of free-text addresses to the OS ABP UPRN database.

    Parameters
    ----------
    input_csv : str, or pandas.DataFrame
        Path to the csv file. The file needs to have two fields in the header ['input_id', 'input_address']
    db_path : str
        Path to the database built. See `flap.create_db()`
    output_file_path : str, default None
        Path for saving the output csv file, containing ['input_id', 'input_address', 'uprn', 'score']. If None, results
        are not saved
    raw_output_path : str, default None
        Path for save the batched raw output files. If None, results are not saved    in_progress_log_path
    max_log_interval: str, default 4800
        The interval under which the programme thinks some process is actively working on it
    batch_size : int, default 10000
        Size of each batch
    max_workers : int, default None
        Number of processes. If None, the max cpu available is determined by `flap.utils.cpu_count.available_cpu_count()`
    in_memory_db : bool, default False
        If in-memory SQLite database is used. If True, a temp database is created in shared memory cache from pre-built
        csv files
    classifier_model_path : str, default None
        The path to the pretrained sklearn classifier model.
        If None, the model is loaded from 'flap.__file__/model/*.clf'
    input_address_col: str, default 'input_address'
        The column name for input addresses
    uprn_col: str, default 'uprn'
        The column name for input UPRN
    Returns
    -------
    pandas.DataFrame
        Score results
    """
    
    # Initialise parameters

    # if output_file_path is None:
    #     output_file_path = os.path.join(os.getcwd(), 'scoring_output.csv')

    if raw_output_path is not None:

        if not os.path.exists(raw_output_path):
            os.mkdir(raw_output_path)

    if in_progress_log_path is not None:

        if not os.path.exists(in_progress_log_path):
            os.mkdir(in_progress_log_path)

    if max_workers is None:
        max_workers = available_cpu_count()

    # Check and read the input

    if isinstance(input_csv, str):
        total_tasks = csv_row_counter(input_csv) - 1
        batch_size = min(batch_size, total_tasks)
        batch_size_adj = int(batch_size / max_workers) * max_workers + max_workers
        total_batches = int(total_tasks / batch_size_adj) + int((total_tasks % batch_size_adj) > 0)

        headers = read_csv_header(input_csv)
        assert all(s in headers for s in ['input_id', 'input_address']), \
            'Two columns are required in input csv file: `input_id` and `input_address`'
        batch_gen = pd.read_csv(input_csv, dtype='object', chunksize=batch_size_adj, index_col=0)

    elif isinstance(input_csv, pd.DataFrame):
        total_tasks = len(input_csv)
        batch_size = min(batch_size, total_tasks)
        batch_size_adj = int(batch_size / max_workers) * max_workers + max_workers
        total_batches = int(total_tasks / batch_size_adj) + int((total_tasks % batch_size_adj) > 0)

        headers = input_csv.columns
        assert all(s in headers for s in ['input_id', 'input_address']), \
            'Two columns are required in input csv file: `input_id` and `input_address`'
        batch_gen = generate_chunks_of_dataframe(input_csv, chunk_size=batch_size_adj)

    else:
        raise TypeError('input_csv should be path(str) or pd.DataFrame')

    # Check the database
    if not in_memory_db:
        sql_db = SqlDB(db_path)
        assert sql_db.db_status['table_indexed_built'], 'Database is not indexed, please Build the Database first'

        matcher = SqlMatcher(sql_db, scorer_path=classifier_model_path)
    else:
        sql_db = SqlDB(db_path)

        sql_db_in_memory = SqlDBInMemory()

        csv_files = [os.path.join(sql_db.sub_paths['csv'], file) for file in os.listdir(sql_db.sub_paths['csv'])]
        csv_names = [os.path.basename(file).split('.')[0]
                     for file in os.listdir(sql_db.sub_paths['csv'])]

        assert all([s in csv_names for s in ['indexed', 'expanded']]), 'CSV database does not exist'

        for table_name, path in zip(csv_names, csv_files):
            print(f'Loading Table {table_name} in memory')
            sql_db_in_memory.load_csv(path, table_name)
            print()

        parser = RuleParserFast(sql_db)

        matcher = SqlMatcher(sql_db_in_memory, parser=parser, scorer_path=classifier_model_path)

    # Main scoring loop

    batch_index = 0

    res_collection = []

    while True:

        try:
            batch_name = 'batch_%s.csv' % batch_index

            batch_exists = False

            batch_in_progress = False

            if raw_output_path is not None:
                batch_path = os.path.join(raw_output_path, batch_name)
                batch_exists = os.path.exists(batch_path)

            if in_progress_log_path is not None:

                log_path = os.path.join(in_progress_log_path, batch_name)
                log_exists = os.path.exists(log_path)

                if not log_exists:

                    with open(log_path, 'w') as f:
                        f.write('%s' % time.time())

                else:

                    with open(log_path, 'r') as f:
                        log_time = float(f.read())

                    if (time.time() - log_time) > max_log_interval:

                        with open(log_path, 'w') as f:
                            f.write('%s' % time.time())

                    else:

                        batch_in_progress = True

            df_batch = next(batch_gen).copy()

            print('Processing %s out of (%s/%s)' % (batch_name, batch_index + 1, total_batches))

            if (not batch_exists) and (not batch_in_progress) and (len(df_batch) > 0):

                mapper = {input_address_col: 'input_address', uprn_col: 'uprn'}
                rev_mapper = {'input_address': input_address_col, 'uprn': uprn_col}
                df_batch.rename(mapper, axis='columns', inplace=True)

                chunk_size = int(batch_size / max_workers) + 1

                res = matcher.score_matching_of_batch(df_batch, input_address_col='input_address', uprn_col='uprn',
                                                      max_workers=max_workers, chunksize=chunk_size)

                res.rename(rev_mapper, axis='columns', inplace=True)

                if raw_output_path is not None:
                    batch_path = os.path.join(raw_output_path, batch_name)
                    res.to_csv(batch_path)
                else:
                    res_collection.append(res.copy())

            batch_index += 1

        except StopIteration:
            print('Scoring Finished, start summarising results')
            break

    if raw_output_path is not None:
        results = _load_all_csv_from_path(raw_output_path, dtype='object')
    else:
        results = pd.concat(res_collection)

    if output_file_path is not None:
        results.to_csv(output_file_path)
        print('Results can be see at: %s' % output_file_path)

    return results
