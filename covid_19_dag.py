# -*- coding: utf-8 -*-


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
    'start_date': datetime(2020, 5, 13),
    'end_date': None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('covid_19', default_args=default_args, schedule_interval= '30 19 * * *')

global_case_sh = BashOperator(
    task_id='JHU_global_case_scrape',
    bash_command="python3 /home/ec2-user/COVID/JHU_daily_global_case_parse.py ",
    queue="pipeline2",
    dag=dag)
case_death_sh = BashOperator(
    task_id='case_death_race_ethnicity_scrape',
    bash_command="python3 /home/ec2-user/COVID/case_death_race_ethnicity_scrape.py ",
    queue="pipeline2",
    dag=dag)




global_case_sh.set_downstream(case_death_sh)
