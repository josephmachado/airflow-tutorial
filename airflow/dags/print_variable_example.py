from airflow.sdk import DAG, Variable
from airflow.decorators import dag, task
from datetime import datetime


@dag(
    dag_id="print_sample_variable",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["example"],
)
def print_sample_variable_dag():
    @task
    def print_variable():
        value = Variable.get("sample_variable")
        print(f"sample_variable = {value}")

    print_variable()


print_sample_variable_dag()

