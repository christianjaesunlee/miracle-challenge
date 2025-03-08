from datetime import datetime
import os

from scraper.functions import run_clinical_trials_scraper, run_eudract_scraper, update_us, update_eu, update_combined

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    # we can optionally set number of retries here
}

with DAG(
    dag_id="webscraper_dag",
    default_args=default_args,
    description="Scrape data and add to MySQL Database",
    start_date=datetime(2023, 1, 1),
    schedule_interval="0 */12 * * *",  # Runs every 12 hours
    catchup=False,
) as dag:
    db_host = os.environ.get("DB_HOST", "localhost")
    db_user = os.environ.get("DB_USER", "root")
    db_password = os.environ.get("DB_PASSWORD", "")
    db_name = os.environ.get("DB_NAME", "")
    backup_dir = os.environ.get("DOWNLOAD_DIR", "")

    # using ts_nodash instead of ds_nodash because we run this twice a day
    backup_cmd = f"""
        mysqldump --no-tablespaces \
          -h {db_host} \
          -u {db_user} \
          -p{db_password} \
          {db_name} \
          > {backup_dir}/mysql_snapshot_{{{{ ts_nodash }}}}.sql
        """

    backup_task = BashOperator(
        task_id="backup_mysql",
        bash_command=backup_cmd
    )

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
    combined_update_task >> backup_task # might also make sense to instead backup the database first instead of last
