from airflow.decorators import task
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

from tools import load_and_clean, get_data_as_json, get_values, get_transformed_data

import os, json

@task()
def extract():
    """Extract data from jobs.csv."""
    data = load_and_clean(os.path.join('source', 'jobs.csv'))
    for i, row in data.iterrows():
        with open(os.path.join('staging', 'extracted', f'{i}.txt'), 'w') as f:
            f.write(row['context'])
        f.close()


@task()
def transform():
    """Clean and convert extracted elements to json."""
    data_as_json = get_data_as_json()
    transformed_data = get_values(data_as_json)
    i = 0
    for data in transformed_data:
        with open(os.path.join('staging', 'transformed', f'{i}.json'), 'w') as f:
            json.dump(data, f, indent=4)
        f.close()
        i += 1
    

@task()
def load():
    """Load data to sqlite database."""
    sqlite_hook = SqliteHook(sqlite_conn_id='sqlite_default')
    transformed_data = get_transformed_data()
    prepare_data = {}
    for key in transformed_data[0].keys():
        prepare_data[key] = []
    for data in transformed_data:
        for table, row in data.items():
            prepare_data[table].append(row)
    
    for table, load_data in prepare_data.items():
        sqlite_hook.insert_rows(table=table, rows=load_data, target_fields=load_data[0].keys())
