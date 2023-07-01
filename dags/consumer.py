"""
DAG is triggered by the Dataset file updates from producer.py. It only
reads the first file of the two. The DAG will always wait for both two
to be updated, not one or the other.
"""

from datetime import datetime

from airflow import DAG
from airflow.datasets import Dataset
from airflow.decorators import task


my_file = Dataset('/tmp/my_file.txt')
my_file_2 = Dataset('/tmp/my_file_2.txt')


with DAG(
    dag_id='consumer',
    schedule=[my_file, my_file_2],
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['Practice', 'Producer-Consumer'],
):

    @task
    def read_dataset() -> None:
        with open(my_file.uri, 'r') as f:
            print(f.read())

    read_dataset()
