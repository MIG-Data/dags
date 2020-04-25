import airflow
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.sensors.http_sensor import HttpSensor
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.contrib.operators.databricks_operator import DatabricksSubmitRunOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 4, 24),
    'end_date': None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('CA_DPH_COVID', default_args=default_args, schedule_interval= '@daily')

five_sh = BashOperator(
    task_id='SCRAPE',
    bash_command="source /home/ec2-user/Scrapes/.venv/bin/activate && python /home/ec2-user/Scrapes/HCSG/PYTHON/Jpb_posts.py ",
    queue="pipeline1",
    dag=dag)
