# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:02:41 2020
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
    'start_date': datetime(2021,2,16),
    'end_date': None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('IHME', default_args=default_args, schedule_interval= '0 0 * * *')
dag2 = DAG('IHME2', default_args=default_args, schedule_interval= '0 0 * * *')
dag3 = DAG('Covidtracking', default_args=default_args, schedule_interval= '0 0 * * *')
dag4 = DAG('flightradar', default_args=default_args, schedule_interval= '0 0 * * *')
dag5 = DAG('MTA', default_args=default_args, schedule_interval= '0 0 * * *')
dag6 = DAG('KFF', default_args=default_args, schedule_interval= '0 12 * * MON')
       
ihme_sh = BashOperator(
    task_id='SCRAPE',
    bash_command="source /home/ec2-user/.venv/bin/activate && python /home/ec2-user/IHME/ihme.py ",
    queue="pipeline5",
    dag=dag)

ihme_sh2 = BashOperator(
    task_id='SCRAPE',
    bash_command="source /home/ec2-user/.venv/bin/activate && python /home/ec2-user/IHME/ihme_summary.py ",
    queue="pipeline5",
    dag=dag2)

covid_sh = BashOperator(
    task_id='Covidtracking',
    bash_command="source /home/ec2-user/.venv/bin/activate && python /home/ec2-user/IHME/covidtracking.py ",
    queue="pipeline5",
    dag=dag3)

covid_ltc_sh = BashOperator(
    task_id='Covidtracking_LTC',
    bash_command="source /home/ec2-user/.venv/bin/activate && python /home/ec2-user/IHME/covidtracking_LTC.py ",
    queue="pipeline5",
    dag=dag3)

flight_sh = BashOperator(
    task_id='Flightradar',
    bash_command="source /home/ec2-user/.venv/bin/activate && python /home/ec2-user/IHME/flightradar.py ",
    queue="pipeline5",
    dag=dag4)

mta_sh = BashOperator(
    task_id='MTA',
    bash_command="source /home/ec2-user/.venv/bin/activate && python /home/ec2-user/IHME/mta.py ",
    queue="pipeline5",
    dag=dag5)

kff_sh = BashOperator(
    task_id='SCRAPE',
    bash_command="source /home/ec2-user/.venv/bin/activate && python /home/ec2-user/IHME/kff.py ",
    queue="pipeline5",
    dag=dag6)
