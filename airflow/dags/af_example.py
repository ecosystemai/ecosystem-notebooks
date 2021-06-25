from datetime import timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import af_example
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'email': ['ramsay@ecosystem.com'],
	'email_on_failure': True,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=1),
	# 'queue': 'bash_queue',
	# 'pool': 'backfill',
	# 'priority_weight': 10,
	# 'end_date': datetime(2016, 1, 1),
	# 'wait_for_downstream': False,
	# 'dag': dag,
	# 'sla': timedelta(hours=2),
	# 'execution_timeout': timedelta(seconds=300),
	# 'on_failure_callback': some_function,
	# 'on_success_callback': some_other_function,
	# 'on_retry_callback': another_function,
	# 'sla_miss_callback': yet_another_function,
	# 'trigger_rule': 'all_success'
}
with DAG(
	'af_example',
	default_args=default_args,
	description='Airflow Example',
	schedule_interval=timedelta(days=1),
	start_date=days_ago(2),
	tags=['example'],
	params={
		"url": "http://demo.ecosystem.ai:3001/api",
		"username": "user@ecosystem.ai",
		"password": "password"
	},
) as dag:
	process_list_collections = PythonOperator(dag=dag,
		task_id='list_collections',
		python_callable=af_example.list_collections,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)
	process_read_data = PythonOperator(dag=dag,
		task_id='read_data',
		python_callable=af_example.read_data,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	process_list_collections >> [process_read_data]