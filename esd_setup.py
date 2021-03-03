import ecosystem_scoring_pdash
from runtime import access
from prediction import jwt_access

runtime_url = "http://127.0.0.1:8091"
pred_url = "http://127.0.0.1:3001/api"
pred_username = "admin@ecosystem.ai"
pred_pass = "password"
auth = access.Authenticate(runtime_url)
p_auth = jwt_access.Authenticate(pred_url, pred_username, pred_pass)

def setup():

	# path where files are located on calling system
	local_file_path = "C:/Users/Ramsay/Documents/GitHub/data/fnb/runtime-wellness-score/"
	target_path="/"
	database = "fnb"

	model_path = local_file_path + model
	model = "GBM_5_AutoML_20200715_160601.zip"

	fs_path = local_file_path + feature_store_file 
	feature_store = "wellnessFeatureStore"
	feature_store_file = "wellnessFeatureStore.csv"

	ad_path = local_file_path + additional_file
	additional = "wellnessScoreMethods"
	additional_file = "wellnessScoreMethods.json"
	ecosystem_scoring_pdash.create_use_case(auth, p_auth, target_path, database, model_path, model, fs_path, feature_store, feature_store_file, ad_path=None, additional=None, additional_file=None)

# 0---------------------------------------------------------------------------------
	# use_case_name = "spending_personality"
	# # path where files are located on calling system
	# local_file_path ="C:/Users/Ramsay/Documents/GitHub/data/fnb/runtime-spend-score/"
	# # target_path="/Users/ecosystem/data/aws_server_properties/fnb/runtime-spend-score/tmp/"
	# target_path="/"
	# database = "fnb"
	# key_field = "CUST_NO"
	# function = ecosystem_scoring_pdash.SPENDING_PERSONALITY
	# model = "GBM_5_AutoML_20200715_160601.zip"

	# feature_store = "fnbPrismFeatureStore20201"
	# feature_store_file = "fnbPrismFeatureStore20201.csv"

	# additional = "spendScoreInterventions"
	# additional_file = "spendScoreInterventions.json"

	# ecosystem_scoring_pdash.create_use_case(auth, p_auth, use_case_name, local_file_path, target_path, database, model, key_field, function, feature_store, feature_store_file, additional=additional, additional_file=additional_file)

setup()