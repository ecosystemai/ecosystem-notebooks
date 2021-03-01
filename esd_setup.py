import ecosystem_scoring_pdash
from runtime import access
from prediction import jwt_access

runtime_url = "http://127.0.0.1:8091"
pred_url = "http://127.0.0.1:4000/api"
pred_username = "admin@ecosystem.ai"
pred_pass = "password"
auth = access.Authenticate(runtime_url)
p_auth = jwt_access.Authenticate(pred_url, pred_username, pred_pass)

def setup():
	use_case_name = "financial_wellness"
	# path where files are located on calling system
	local_file_path = "C:/Users/Ramsay/Documents/GitHub/data/fnb/runtime-wellness-score/"
	target_path="/"
	database = "fnb"
	key_field = "CUST_NO"
	function = ecosystem_scoring_pdash.FINANCIAL_WELLNESS

	model = "GBM_5_AutoML_20200715_160601.zip"

	feature_store = "wellnessFeatureStore"
	feature_store_file = "wellnessFeatureStore.csv"

	additional = "wellnessScoreMethods"
	additional_file = "wellnessScoreMethods.json"

	properties = """
	logging.level=4
	date.format=yyyy-MM-dd'T'HH:mm:ss.SSSSSSXXX
	logger.level=500

	mongo.secure.data=true
	mongo.ecosystem.user=ecosystem_user
	mongo.port=54446
	mongo.server=localhost
	mongo.ecosystem.password=EcoEco321
	mongo.connect=mongodb://ecosystem_user:EcoEco321@localhost:54446/?authSource=admin
	mongo.authentication.source=admin
	logging.database=logging
	logging.collection=ecosystemruntime
	logging.collection.response=ecosystemruntime_response
	logging.detail=false
	user.profiles=profilesMaster

	# Prediction case settings
	predictor.name=financial_wellness
	user.data=/
	user.generated.models=/

	# Plugin Loader for Pre- and post-scoring logic or interventions
	plugin.prescore=com.ecosystem.plugin.customer.PrePredictCustomer
	plugin.postscore=com.ecosystem.plugin.customer.PostScoreFinancialWellness

	# MOJO keys are loaded into memory and be reloaded with the /reload endpoint
	# The sequence is important as first model in list is referenced 1, and second as 2 etc.
	mojo.key=GBM_5_AutoML_20200715_160601.zip

	# Features
	# set default params to retrieve if key fails with lookup:{key:'msisdn',value:123}
	# change value:123 to the default key from the feature store
	predictor.param.lookup={predictor:'financial_wellness',mojo:1,database:'mongodb',db:'fnb',table:'wellnessFeatureStore',lookup:{key:'CUST_NO',value:123},result:{parm1:'field1', parm2:'field2'}}
	predictor.param.lookup.features=saveScore,rtiScore,prismScore,productiveSpendScore
	predictor.corpora=[{name:'wellness_score_methods',database:'mongodb',db:'fnb',table:'wellnessScoreMethods'}]

	predictor.offercache=0
	predictor.epsilon=0.05
	"""
	ecosystem_scoring_pdash.create_use_case(auth, p_auth, use_case_name, local_file_path, target_path, database, model, key_field, function, feature_store, feature_store_file, properties, additional=additional, additional_file=additional_file)

	use_case_name = "spending_personality"
	# path where files are located on calling system
	local_file_path ="C:/Users/Ramsay/Documents/GitHub/data/fnb/runtime-spend-score/"
	# target_path="/Users/ecosystem/data/aws_server_properties/fnb/runtime-spend-score/tmp/"
	target_path="/"
	database = "fnb"
	key_field = "CUST_NO"
	function = ecosystem_scoring_pdash.SPENDING_PERSONALITY
	model = "GBM_5_AutoML_20200715_160601.zip"

	feature_store = "fnbPrismFeatureStore20201"
	feature_store_file = "fnbPrismFeatureStore20201.csv"

	additional = "spendScoreInterventions"
	additional_file = "spendScoreInterventions.json"

	properties = """
	logging.level=4
	date.format=yyyy-MM-dd'T'HH:mm:ss.SSSSSSXXX
	logger.level=500

	mongo.secure.data=true
	mongo.ecosystem.user=ecosystem_user
	mongo.port=54446
	mongo.server=localhost
	mongo.ecosystem.password=EcoEco321
	mongo.connect=mongodb://ecosystem_user:EcoEco321@localhost:54446/?authSource=admin
	mongo.authentication.source=admin
	logging.database=logging
	logging.collection=ecosystemruntime
	logging.collection.response=ecosystemruntime_response
	logging.detail=false
	user.profiles=profilesMaster

	# Prediction case settings
	predictor.name=spending_personality
	user.data=/
	user.generated.models=/

	# Plugin Loader for Pre- and post-scoring logic or interventions
	plugin.prescore=com.ecosystem.plugin.customer.PrePredictCustomer
	plugin.postscore=com.ecosystem.plugin.customer.PostScoreSpendingPersonality

	# MOJO keys are loaded into memory and be reloaded with the /reload endpoint
	# The sequence is important as first model in list is referenced 1, and second as 2 etc.
	mojo.key=GBM_5_AutoML_20200715_160601.zip

	# Features
	# set default params to retrieve if key fails with lookup:{key:'msisdn',value:123}
	# change value:123 to the default key from the feature store
	predictor.param.lookup={predictor:'spending_personality',mojo:1,database:'mongodb',db:'fnb',table:'fnbPrismFeatureStore20201',lookup:{key:'CUST_NO',value:123},result:{parm1:'field1', parm2:'field2'}}
	predictor.param.lookup.features=personalityType,15428Spend,15696Spend,15313Spend,15313Frequency,CUST_REC_OPEN_DATE,ExperientialSpend,BOND_IND,5541Spend,RGN_CDE,CUST_AGE,Prepaid_BuyFrequency,15654Spend,TransfersFrequency,15691Frequency,CUST_TOT_DR_BALs,TransfersSpend,NO_WES_ACCT,15312Spend,6545Spend,15751Spend,15751Frequency,1FrequencyN,EssentialSpend,EMPLOYER_NAME,IntrovertSpend

	predictor.corpora=[{name:'spending_personality_intervention',database:'mongodb',db:'fnb',table:'spendScoreInterventions'}]

	predictor.offercache=0
	predictor.epsilon=0.05
	"""

	ecosystem_scoring_pdash.create_use_case(auth, p_auth, use_case_name, local_file_path, target_path, database, model, key_field, function, feature_store, feature_store_file, properties, additional=additional, additional_file=additional_file)

setup()