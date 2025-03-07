from datetime import datetime

from scraper.functions import run_clinical_trials_scraper, run_eudract_scraper, update_us, update_eu, update_combined

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    # we can optionally set number of retries here
}

with DAG(
    dag_id="my_dag",
    default_args=default_args,
    description="Scrape data and add to MySQL Database",
    start_date=datetime(2023, 1, 1),
    schedule_interval="0 */12 * * *",  # Runs every 12 hours
    catchup=False,
) as dag:

    us_scraper_task = PythonOperator(
        task_id="us_scraper_task",
        python_callable=run_clinical_trials_scraper
    )

    eu_scraper_task = PythonOperator(
        task_id="eu_scraper_task",
        python_callable=run_eudract_scraper
    )

    us_update_task = PythonOperator(
        task_id="us_update_task",
        python_callable=update_us
    )

    eu_update_task = PythonOperator(
        task_id="eu_update_task",
        python_callable=update_eu
    )

    combined_update_task = PythonOperator(
        task_id="combined_update_task",
        python_callable=update_combined
    )

    eu_scraper_task >> us_scraper_task # XXX: adding this dependency because these tasks seem to compete for resources
    us_scraper_task >> us_update_task
    eu_scraper_task >> eu_update_task
    [us_update_task, eu_update_task] >> combined_update_task
