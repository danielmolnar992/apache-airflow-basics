"""
Passing values between tasks and using branch to decide which path to take.
- Using XCom to push and pull key-value pairs.
- A branch operator decides which task is to be executed next.
- Trigger rule starts the closing task at the end of either path.
"""

from datetime import datetime

from airflow import DAG
from airflow.models.taskinstance import TaskInstance
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator


def _t1(ti: TaskInstance) -> None:
    ti.xcom_push(key='random_value', value=42)


def _t2(ti: TaskInstance) -> None:
    random_value = ti.xcom_pull(key='random_value', task_ids='create_value')
    print(f'Printing the pulled value: {random_value}')


def _branch(ti: TaskInstance) -> str:
    """Depending on the value, it directs the flow different tasks."""

    value = ti.xcom_pull(key='random_value', task_ids='create_value')

    if value == 42:
        return 'expected_value'

    return 'unexpected_value'


with DAG(
    'xcom_dag',
    start_date=datetime(2022, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['Practice', 'XCom'],
) as dag:

    create_value = PythonOperator(
        task_id='create_value',
        python_callable=_t1
    )

    branch = BranchPythonOperator(
        task_id='branch',
        python_callable=_branch
    )

    expected_value = PythonOperator(
        task_id='expected_value',
        python_callable=_t2
    )

    unexpected_value = BashOperator(
        task_id='unexpected_value',
        bash_command="echo 'This is an unexpected value.'"
    )

    closing_task = BashOperator(
        task_id='closing_task',
        bash_command="echo 'Closing task finished successfully.'",
        trigger_rule='none_failed_min_one_success'
    )

    (create_value
        >> branch
        >> [expected_value, unexpected_value]
        >> closing_task)
