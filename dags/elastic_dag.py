from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from hooks.elastic.elastic_hook import ElasticHook


def _print_es_info() -> None:
    elastic_hook = ElasticHook()
    print(f'Elastic hook info: {elastic_hook.info()}')


with DAG(
    'elastic_dag',
    start_date=datetime(2022, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['Elastic'],
) as dag:

    print_es_info = PythonOperator(
        task_id='print_es_info',
        python_callable=_print_es_info
    )
