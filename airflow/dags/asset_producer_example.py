"""
Asset-Based DAGs — Airflow 3

producer_dag : runs every hour, processes data and updates an Asset
consumer_dag : no time-based schedule — triggered automatically by the
               scheduler whenever the Asset is updated by the producer
"""

import pendulum
from airflow.sdk import dag, task, Asset, get_current_context


# ── Shared Asset definition ────────────────────────────────────────────────
# Both DAGs reference the same Asset object.
# The URI is just a logical identifier — Airflow doesn't access it directly.
hourly_report = Asset("s3://my-bucket/hourly-report/data.json")


# ── Producer DAG ───────────────────────────────────────────────────────────
@dag(
    dag_id="producer_dag",
    schedule="@hourly",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    tags=["asset", "producer"],
)
def producer_dag():
    @task()
    def extract() -> dict:
        """Fake extraction step."""
        return {"rows": 42, "source": "orders_db"}

    @task(outlets=[hourly_report])  # <-- marks the asset as updated on success
    def transform_and_write(raw: dict) -> None:
        """
        Transform and write data.
        Declaring outlets=[hourly_report] tells Airflow that when this
        task succeeds, the asset has been updated — which triggers the
        consumer DAG automatically.
        """
        context = get_current_context()
        start = context["data_interval_start"]
        end = context["data_interval_end"]

        print(f"Writing report for interval: {start} → {end}")
        print(f"Processed {raw['rows']} rows from {raw['source']}")
        print(f"Asset updated: {hourly_report.uri}")

    raw = extract()
    transform_and_write(raw)


producer_dag()
