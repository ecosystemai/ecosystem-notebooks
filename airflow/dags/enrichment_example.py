from datetime import timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import enrichment
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
	'enrichment_example',
	default_args=default_args,
	description='Feature store enrichment examples.',
	schedule_interval=timedelta(days=1),
	start_date=days_ago(2),
	tags=['example'],
	params={
		"url": "http://demo.ecosystem.ai:3001/api",
		"username": "user@ecosystem.ai",
		"password": "password",
		"prepare": {
			"cpr": "pre test1",
			"enrich": "pre test2",
			"tsf": "pre test3",
			"en": "pre test4",
			"apr": "pre test5",
			"fore": "pre test6",
			"pred": "pre test7"
		},
		"enrichment": {
			"cpr": {
				"collection": "bank_transactions",
				"collectionOut": "bank_transactions_CLIENT_PULSE_RELIABILITY_process_1",
				"database": "master",
				"find": "{customer:590}",
				"groupby": "mcc_category",
				"mongoAttribute": "trns_amt",
				"type": "reliability"
			},
			"enrich": {
				"category": "trns_amt",
				"collection": "bank_transactions",
				"collectionOut": "bank_transactions_PERSONALITY_process_1",
				"database": "master",
				"find": "{customer:590}",
				"groupby": "customer"
			},
			"tsf": {
				"categoryfield": "mcc_category",
				"collection": "bank_transactions",
				"database": "master",
				"datefield": "effReformatted",
				"featureset": "bank_transactions_TIME_SERIES_process_1",
				"find": "{customer:590}",
				"groupby": "customer",
				"numfield": "trns_amt"
			},
			"en": {
				"collection": "bank_transactions",
				"collectionOut": "bank_transactions_ECOGENETIC_process_1",
				"database": "master",
				"find": "{cusomter:590}",
				"graphMeta": '{"vertex":["customer","mcc_category", "trns_type"],"edges":[{"from":"customer","to":"mcc_category"},{"from":"mcc_category","to":"trns_type"}]}',
				"graphParam": "{}"
			},
			"apr": {
				"colItem": "bank_transactions",
				"collection": "bank_transactions",
				"collectionOut": "bank_transactions_BASKET_process_1",
				"custField": "customer",
				"database": "master",
				"dbItem": "master",
				"find": "{customer:590}",
				"itemField": "mcc_category",
				"supportCount": 2
			},
			"fore": {
				"attribute": "trns_amt",
				"collection": "bank_transactions",
				"collectionOut": "bank_transactions_FORECAST_process_1",
				"database": "master",
				"dateattribute": "effReformatted",
				"find": "{customer:590}",
				"historicsteps": 50,
				"steps": 10
			},
			"pred": {
				"attributes": "GBM_4_AutoML_20210518_142905_job",
				"collection": "bank_full_1",
				"limit": "1000000",
				"mongodb": "master",
				"predictor": "GBM_4_AutoML_20210518_142905",
				"predictor_label": "GBM_4_AutoML_20210518_142905_job",
				"search": "{}",
				"skip": "{}",
				"sort": "{}"
			}
		}
	},	
) as dag:
	preprocess_cpr = PythonOperator(dag=dag,
		task_id='preprocess_client_pulse_reliability',
		python_callable=enrichment.preprocess_client_pulse_reliability,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	process_cpr = PythonOperator(dag=dag,
		task_id='process_client_pulse_reliability',
		python_callable=enrichment.process_client_pulse_reliability,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	preprocess_enrich = PythonOperator(dag=dag,
		task_id='preprocess_personality_enrich',
		python_callable=enrichment.preprocess_personality_enrich,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	process_enrich = PythonOperator(dag=dag,
		task_id='personality_enrich',
		python_callable=enrichment.personality_enrich,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	preprocess_tsf = PythonOperator(dag=dag,
		task_id='preprocess_generate_time_series_features',
		python_callable=enrichment.preprocess_generate_time_series_features,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	process_tsf = PythonOperator(dag=dag,
		task_id='generate_time_series_features',
		python_callable=enrichment.generate_time_series_features,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	preprocess_en = PythonOperator(dag=dag,
		task_id='preprocess_ecogenetic_network',
		python_callable=enrichment.preprocess_ecogenetic_network,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	process_en = PythonOperator(dag=dag,
		task_id='process_ecogenetic_network',
		python_callable=enrichment.process_ecogenetic_network,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	preprocess_apr = PythonOperator(dag=dag,
		task_id='preprocess_apriori',
		python_callable=enrichment.preprocess_apriori,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	process_apr = PythonOperator(dag=dag,
		task_id='process_apriori',
		python_callable=enrichment.process_apriori,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	preprocess_fore = PythonOperator(dag=dag,
		task_id='preprocess_generate_forecast',
		python_callable=enrichment.preprocess_generate_forecast,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	process_fore = PythonOperator(dag=dag,
		task_id='generate_forecast',
		python_callable=enrichment.generate_forecast,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)
	
	preprocess_pred = PythonOperator(dag=dag,
		task_id='preprocess_prediction_enrich',
		python_callable=enrichment.preprocess_prediction_enrich,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	process_pred = PythonOperator(dag=dag,
		task_id='prediction_enrich',
		python_callable=enrichment.prediction_enrich,
		op_args=[],
		provide_context=True
		# op_kwargs={'keyword_argument':'which will be passed to function'}
	)

	preprocess_cpr >> [process_cpr]
	preprocess_enrich >> [process_enrich]
	preprocess_tsf >> [process_tsf]
	preprocess_en >> [process_en]
	preprocess_apr >> [process_apr]
	preprocess_fore >> [process_fore]
	preprocess_pred >> [process_pred]