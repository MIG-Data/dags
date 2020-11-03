# -*- coding: utf-8 -*-
"""
Created on Mon Nov 2 14:02:41 2020

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
    'start_date': datetime(2020, 11, 1),
     'end_date' : None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 5,
	'wait_for_downstream': True,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('Keepa_Amazon_dag', default_args=default_args, schedule_interval= '30 12 * * sun,mon,tue,wed,thu,fri,sat ')


amazon_scrape = BashOperator(
    task_id='keepa_amazon',
    bash_command="python3 /home/ec2-user/AMAZON/Keepa_API.py",
    email_on_failure = True,
    email = email_list,
    queue='pipeline9',
    dag=dag)


