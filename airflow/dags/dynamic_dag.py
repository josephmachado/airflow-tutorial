"""
Simple Dynamic DAG — Airflow 3
Demonstrates dynamic task mapping with .expand()
Each item in the list gets its own task instance at runtime.
"""

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="simple_dynamic_dag",
    schedule="@daily",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    tags=["dynamic", "example"],
)
def simple_dynamic():
    @task()
    def get_items() -> list[str]:
        """
        Returns the list of items to process.
        In practice this could come from a DB, API, config file, etc.
        """
        return ["orders", "customers", "products"]

    @task()
    def process(table: str) -> str:
        """
        This task is dynamically mapped — one instance per item.
        Airflow creates 3 task instances at runtime:
          process-orders, process-customers, process-products
        """
        result = f"Processed table: {table.upper()}"
        print(result)
        return result

    @task()
    def summarise(results: list[str]) -> None:
        """Receives all mapped outputs as a single list."""
        print("Summary:")
        for r in results:
            print(f"  ✓ {r}")

    items = get_items()

    # .expand() is what makes it dynamic —
    # one task instance is created per element in `items`
    processed = process.expand(table=items)

    summarise(processed)


simple_dynamic()
