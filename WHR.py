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
    'start_date': datetime(2020, 12, 24),
    'end_date': None,
    'email': ['tcai@migcap.com', 'yjeon@migcap.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('WHR', default_args=default_args, schedule_interval= '1 0,12 * * *')

HD_sh = BashOperator(
    task_id='HD',
    bash_command="source /home/ec2-user/Scrapes/.venv/bin/activate && python /home/ec2-user/Scrapes/WHR/PYTHON/Homedepot.py ",
    queue="pipeline1",
    dag=dag)

HD_LT_sh = BashOperator(
    task_id='HD_LT',
    bash_command="source /home/ec2-user/Scrapes/.venv/bin/activate && python /home/ec2-user/Scrapes/WHR/PYTHON/Homedepot_LT.py ",
    queue="pipeline1",
    dag=dag)
    
LOW_sh = BashOperator(
    task_id='LOW',
    bash_command="source /home/ec2-user/Scrapes/.venv/bin/activate && python /home/ec2-user/Scrapes/WHR/PYTHON/Lowes_mb.py ",
    queue="pipeline1",
    dag=dag)
    
LOW_sh = BashOperator(
    task_id='LOW_LT',
    bash_command="source /home/ec2-user/Scrapes/.venv/bin/activate && python /home/ec2-user/Scrapes/WHR/PYTHON/Lowes_LT.py ",
    queue="pipeline1",
    dag=dag)

WHR_COM_sh = BashOperator(
    task_id='WHR_COM',
    bash_command="source /home/ec2-user/Scrapes/.venv/bin/activate && python /home/ec2-user/Scrapes/WHR/PYTHON/WHR_COM.py ",
    queue="pipeline1",
    dag=dag)
