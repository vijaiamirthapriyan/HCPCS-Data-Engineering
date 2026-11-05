from datetime import datetime
import logging
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_SRC = "/opt/airflow/project_src"
sys.path.insert(0, PROJECT_SRC)

from scraper import main as scrape_main
from validate_raw import main as validate_main
from transform import main as transform_main
from data_quality import main as data_quality_main
from scd2_load import main as scd2_main


def log_task_start(task_name):
    logging.info("Starting task: %s", task_name)


def log_task_success(task_name):
    logging.info("Task completed successfully: %s", task_name)


def run_with_logging(task_name, function):
    logging.info("Starting task: %s", task_name)
    try:
        function()
        logging.info("Task completed successfully: %s", task_name)
    except Exception:
        logging.exception("Task failed: %s", task_name)
        raise


with DAG(
    dag_id="hcpcs_pipeline",
    description="HCPCS scrape, validate, transform, quality check, and SCD2 load",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["hcpcs", "data-engineering"],
) as dag:

    scrape = PythonOperator(
        task_id="scrape_hcpcs",
        python_callable=run_with_logging,
        op_args=["scrape_hcpcs", scrape_main],
    )

    validate = PythonOperator(
        task_id="validate_raw_data",
        python_callable=run_with_logging,
        op_args=["validate_raw_data", validate_main],
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=run_with_logging,
        op_args=["transform_data", transform_main],
    )

    data_quality = PythonOperator(
        task_id="data_quality_check",
        python_callable=run_with_logging,
        op_args=["data_quality_check", data_quality_main],
    )

    scd2_load = PythonOperator(
        task_id="scd2_load_to_postgres",
        python_callable=run_with_logging,
        op_args=["scd2_load_to_postgres", scd2_main],
    )

    scrape >> validate >> transform >> data_quality >> scd2_load