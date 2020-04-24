# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 23:54:14 2020

@author: tcai
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 14:02:41 2020

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
    'start_date': datetime(2020, 4, 20),
    'end_date': None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('DE_dag', default_args=default_args, schedule_interval= '@daily')

DE_sh = BashOperator(
    task_id='DE_Equipment_Trader_SCRAPE',
    bash_command="python3 /home/ec2-user/DE/equipment_trader.py ",
    queue="pipeline2",
    dag=dag)


notebook_task_params = {
        'existing_cluster_id': '0128-230140-huts317', # cluster id of MIG Cluster 2
        'notebook_task': {
                'notebook_path': '/Users/garquette@migcap.com/DE_sales_inventory'
                }
        }
DE_notebook_task = DatabricksSubmitRunOperator(
        task_id = 'DE_sales_inventory',
        dag = dag,
        queue = 'pipeline2',
        json = notebook_task_params
        )
DE_sh.set_downstream(DE_notebook_task)
