"""
Simple DAG to save user data from an API endpoint to a file and then load it
into a Postgre table. In the below tag there are examples to:
- Define a Data Pipeline
- Execute a SQL request with the PostgresOperator
- Execute a Python function with the PythonOperator
- Execute an HTTP request against an API
- Wait for something to happen with Sensors
- Use Hooks to access secret methods
- Exchange data between tasks
"""


import json
from datetime import datetime

from airflow import DAG
from airflow.models.taskinstance import TaskInstance
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from pandas import json_normalize


def _process_user(ti: TaskInstance) -> None:
    """Pulls data from task and creates a CSV from JSON."""

    user = ti.xcom_pull(task_ids='extract_user')
    user = user['results'][0]
    processed_user = json_normalize({
        'first_name': user['name']['first'],
        'last_name': user['name']['last'],
        'country': user['location']['country'],
        'username': user['login']['username'],
        'password': user['login']['password'],
        'email': user['email'],
    })

    processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)


def _store_user() -> None:
    """Copies user data from CSV to Postgres table."""

    hook = PostgresHook(postgres_conn_id='postgres')
    hook.copy_expert(
        sql="COPY users FROM stdin WITH DELIMITER AS ','",
        filename='/tmp/processed_user.csv'
    )


with DAG(
    'user_processing',
    schedule='@daily',
    start_date=datetime(2023, 6, 1),
    catchup=False,
    tags=['Practice', 'User Processing'],
) as dag:

    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS users (
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )
        '''
    )

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/'
    )

    extract_user = SimpleHttpOperator(
        task_id='extract_user',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    process_user = PythonOperator(
        task_id='process_user',
        python_callable=_process_user
    )

    store_user = PythonOperator(
        task_id='store_user',
        python_callable=_store_user
    )

    (create_table
        >> is_api_available
        >> extract_user
        >> process_user
        >> store_user)
