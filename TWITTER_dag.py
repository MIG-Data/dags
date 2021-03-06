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
    'start_date': datetime(2020,3,5),
    'end_date': None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('Twitter_dag', default_args=default_args, schedule_interval= '15 20 * * *')

twitter_sh = BashOperator(
    task_id='GET_TSLA_TWEET',
    bash_command="/home/ec2-user/GET_OLD_TWEET/GET_OLD_TWEET_TSLA.sh ",
    queue='pipeline9',
    dag=dag)

Topic_Modeling_sh = BashOperator(
    task_id='Topic_Modeling_Twitter',
    bash_command="/home/ec2-user/GET_OLD_TWEET/Twitter_topic_modeling.sh ",
    queue='pipeline9',
    dag=dag)

twitter_sh.set_downstream(Topic_Modeling_sh)

