# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 23:54:14 2020
@author: yjeon
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
    'start_date': datetime(2021, 4, 14),
    'end_date': None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('BYND', default_args=default_args, schedule_interval= '@weekly')

DE_sh = BashOperator(
    task_id='BYND',
    bash_command="source /home/ec2-user/.venv/bin/activate && python /home/ec2-user/BYND/BYND.py ",
    queue="pipeline5",
    dag=dag)
