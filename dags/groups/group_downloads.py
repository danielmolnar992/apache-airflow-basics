from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup


def download_tasks() -> TaskGroup:

    with TaskGroup('downloads', tooltip='Download tasks') as group:

        BashOperator(
            task_id='download_a',
            bash_command='sleep 2'
        )

        BashOperator(
            task_id='download_b',
            bash_command='sleep 2'
        )

        BashOperator(
            task_id='download_c',
            bash_command='sleep 2'
        )

        return group
