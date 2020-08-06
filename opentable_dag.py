
"""
S3 Sensor Connection Test
"""
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
    'start_date': datetime(2020, 8, 4),
    'end_date': None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

EDT_dag = DAG('OPENTABLE_EDT_dag', default_args=default_args, schedule_interval= '0 2 * * *')
CDT_dag = DAG('OPENTABLE_CDT_dag', default_args=default_args, schedule_interval= '0 3 * * *')
MDT_dag = DAG('OPENTABLE_MDT_dag', default_args=default_args, schedule_interval= '0 4 * * *')
PDT_dag = DAG('OPENTABLE_PDT_dag', default_args=default_args, schedule_interval= '0 5 * * *')

EDT_sh = BashOperator(
    task_id='OPENTABLE_EDT_SCRAPE',
    bash_command="python3 /home/ec2-user/OPENTABLE/Opentable_scraping_aws.py EDT ",
    queue="pipeline5",
    dag=EDT_dag)



CDT_sh = BashOperator(
    task_id='OPENTABLE_CDT_SCRAPE',
    bash_command="python3 /home/ec2-user/OPENTABLE/Opentable_scraping_aws.py CDT ",
    queue="pipeline5",
    dag=CDT_dag)

MDT_sh = BashOperator(
    task_id='OPENTABLE_MDT_SCRAPE',
    bash_command="python3 /home/ec2-user/OPENTABLE/Opentable_scraping_aws.py MDT ",
    queue="pipeline5",
    dag=MDT_dag)

PDT_sh = BashOperator(
    task_id='OPENTABLE_PDT_SCRAPE',
    bash_command="python3 /home/ec2-user/OPENTABLE/Opentable_scraping_aws.py PDT ",
    queue="pipeline5",
    dag=PDT_dag)
