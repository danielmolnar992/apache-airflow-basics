# Apache Airflow Basics

Playing with the basic concepts of Apache Airflow.

## Stack

- Python 3.7
- Docker
- Airflow 2.4 with CeleryExecutor
- Elasticsearch
- Pandas
- Flake8 and Isort for linting and formatting (in local dev environment)

## Usage

1. Run `docker-compose up -d` to install from compose file and run the local server.
2. Airflow is available at `http://127.0.0.1:8080/`.
3. Username and password is `airflow`.
4. Find the description of the DAGs in the `./dag` folder files.
5. Filter for `Practice` tag if examples are enabled in the docker-compose file By default, they are not.
6. Access Celery Flower by at `http://127.0.0.1:5555/`.
    - Running with `docker-compose --profile flower up -d`.
7. Increase the number of workers with `docker-compose up -d --scale airflow-worker=2`.

Note: `elastic` and `airflow-worker-hc` services requires additional resources from the host machine, make sure you give at least 6-7 GBs of RAM and 6-7 CPU cores if you run all at once.

## Practice Projects

By filtering for the given tag, you can find the related tags in the Airflow UI.

---

### User Processing

Tag: `User Processing`

Creates the SQL table to collect data from an API endpoint if available and adds to the table.

Connections:
- postgres:
    - Connection ID: `postgres`
    - Connection Type: `Postgres`
    - Host: `postgres`
    - Port: `5432`
    - Login: `airflow`
    - Password: `airflow`
- user_api
    - Connection ID: `user_api`
    - Connection Type: `HTTP`
    - Host: `https://randomuser.me/`

![User Processing DAG](/static/user_processing_dag.png)

---

### Producer and Consumer

Tag: `Producer-Consumer`

Producer updates two datasets and consumer DAG gets triggered by it.
In the Airflow UI turn on the consumer DAG first and then the producer. You should see that the producer triggers the consumer upon successful execution.

The Datasets are also visible under the Dataset menu in the top left of the UI.
The 'producer update' message is visible in the Grid view -> read_dataset -> Log output.

![Producer and Consumer DAGs](/static/producer_consumer_dags.png)

---

### Parallel DAG

Tag: `Parallel`

Simple example of parallel execution with CeleryExecutor.
The BashExecutors are sleeping for 10 seconds. This is handy to test the Flower UI.

Task `transform` is sent to the `high_cpu` worker.
Enable the second HC worker to pick up the task within the `docker-compose.yaml` as `airflow-worker-hc` service.

![Parallel DAG](/static/parallel_dag.png)

---

### Group DAGs

Tag: `Grouping`

Group DAG groups the tasks with a simple sleep bash command.
This is just to showcase the task group implementation.

![Task Group DAG](/static/task_group_dag.png)

---

### XCom DAG

Tag: `XCom`

An example to show how to share values between tasks with the help of XCom.
- In this dag the first task creates a value.
- This value than passed to a branch based on which it decides if it was expected or not.
    - If expected, then a task logs it.
    - If not, then a different one writes a different log entry.
- In the end the same closing task is performed on either path's end.

![XCom DAG](/static/xcom_dag.png)


### Elasticsearch

Tag: `Elastic`

A custom Elasticsearch hook plugin was created to get the info of the instance and write it into the logs.
Enable the `elastic` service in the docker-compose file if it wasn't.

Connection:
- elastic
    - Connection ID: `elastic_default`
    - Connection Type: `HTTP`
    - Host: `elastic`
    - Port: `9200`

