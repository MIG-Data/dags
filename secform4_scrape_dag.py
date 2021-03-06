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
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 10, 27),
    'end_date': None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('SEC_form4_dag', default_args=default_args, schedule_interval= '@weekly')

secform4_sh = BashOperator(
    task_id='SEC_FORM4_SCRAPE',
    bash_command="python3 /home/ec2-user/secform4_scrape/SEC_API.py ",
    queue="pipeline2",
    dag=dag)

secform4_process_sh = BashOperator(
    task_id='SEC_FORM4_PROCESS',
    bash_command="python3 /home/ec2-user/secform4_scrape/SEC_form4_process.py ",
    queue="pipeline2",
    dag=dag)

secform4_sh.set_downstream(secform4_process_sh)

