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
    'start_date': airflow.utils.dates.days_ago(0),
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('amazon_top100_dag', default_args=default_args, schedule_interval= '30 12 * * sun,mon,tue,wed,thu,fri,sat ')

'''
amazon_scrape = BashOperator(
    task_id='bash_test',
    bash_command="/home/ec2-user/SHELL/AMAZON.sh >> /home/ec2-user/SHELL/log/amazon.log 2>&1 ",
    dag=dag)
'''

notebook_task_params = {
        'existing_cluster_id': '0128-230140-huts317', # cluster id of MIG Cluster 2
        'notebook_task': {
                'notebook_path': '/Users/garquette@migcap.com/amazon_analysis_xbyte'
                }
        }
notebook_task = DatabricksSubmitRunOperator(
        task_id = 'notebook_task',
        dag = dag,
        json = notebook_task_params
        )

