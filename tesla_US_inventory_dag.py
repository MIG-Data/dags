@weekly"""
#'wait_for_downstream': True,Created on Mon Feb 24 14:02:41 2020

@author: tcai
"""

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

email_list = ['tcai@migcap.com', 'yjeon@migcap.com']


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 3, 23),
    'end_date': None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 5,
   
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('tesla_US_inventory_dag', default_args=default_args, schedule_interval= '@weekly')


tesla_US_inventory_scrape = BashOperator(
    task_id='tesla_US_inventory_scrape',
    bash_command="/home/ec2-user/SHELL/tesla.sh ",
    queue = 'pipeline9',
    dag=dag)

