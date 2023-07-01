from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup


def transform_tasks() -> TaskGroup:

    with TaskGroup('transforms', tooltip='Transform tasks') as group:

        BashOperator(
            task_id='transform_a',
            bash_command='sleep 2'
        )

        BashOperator(
            task_id='transform_b',
            bash_command='sleep 2'
        )

        BashOperator(
            task_id='transform_c',
            bash_command='sleep 2'
        )

        return group
