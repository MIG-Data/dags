# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:02:41 2020

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

default_args = {
    'owner': 'MIG',
    'depends_on_past': False,
    'start_date': datetime(2020, 3, 5),
    'end_date' : None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('unb_dag', default_args=default_args, schedule_interval= '0 0 * * *')

six_sh = BashOperator(
    task_id='SCRAPE',
    bash_command="/home/ec2-user/Scrapes/URNERBARRY/SHELL/urnerbarry2.sh ",
    queue='pipeline1',
    dag=dag)

