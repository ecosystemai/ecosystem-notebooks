from prediction.apis import data_management_engine
from prediction.apis import data_munging_engine
from prediction.apis import worker_file_service
from prediction.apis import algorithm_client_pulse
import authenticate

def preprocess_client_pulse_reliability(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	value = kwargs["dag_run"].conf.get("prepare")["__var"]["cpr"]
	print(value)

def process_client_pulse_reliability(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	data = kwargs["dag_run"].conf.get("enrichment")["__var"]["cpr"]["__var"]
	collection = data["collection"]
	collectionOut = data["collectionOut"]
	database = data["database"]
	find = data["find"]
	groupby = data["groupby"]
	mongoAttribute = data["mongoAttribute"]
	rtype = data["type"]
	output = data_munging_engine.process_client_pulse_reliability(p_auth, collection, collectionOut, database, find, groupby, mongoAttribute, rtype)
	print(output)

def preprocess_personality_enrich(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	value = kwargs["dag_run"].conf.get("prepare")["__var"]["enrich"]
	print(value)

def personality_enrich(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	data = kwargs["dag_run"].conf.get("enrichment")["__var"]["enrich"]["__var"]
	category = data["category"]
	collection = data["collection"]
	collectionOut = data["collectionOut"]
	database = data["database"]
	find = data["find"]
	groupby = data["groupby"]
	output = data_munging_engine.personality_enrich(p_auth, category, collection, collectionOut, database, find, groupby)
	print(output)

def preprocess_generate_time_series_features(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	value = kwargs["dag_run"].conf.get("prepare")["__var"]["tsf"]
	print(value)

def generate_time_series_features(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	data = kwargs["dag_run"].conf.get("enrichment")["__var"]["tsf"]["__var"]
	categoryfield = data["categoryfield"]
	collection = data["collection"]
	database = data["database"]
	datefield = data["datefield"]
	featureset = data["featureset"]
	find = data["find"]
	groupby = data["groupby"]
	numfield = data["numfield"]
	output = data_munging_engine.generate_time_series_features(p_auth, categoryfield, collection, database, datefield, featureset, find, groupby, numfield)
	print(output)

def preprocess_ecogenetic_network(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	value = kwargs["dag_run"].conf.get("prepare")["__var"]["en"]
	print(value)

def process_ecogenetic_network(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	data = kwargs["dag_run"].conf.get("enrichment")["__var"]["en"]["__var"]
	collection = data["collection"]
	collectionOut = data["collectionOut"]
	database = data["database"]
	find = data["find"]
	graphMeta = data["graphMeta"]
	graphParam = data["graphParam"]
	output = algorithm_client_pulse.process_ecogenetic_network(p_auth, collection, collectionOut, database, find, graphMeta, graphParam)
	print(output)

def preprocess_apriori(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	value = kwargs["dag_run"].conf.get("prepare")["__var"]["apr"]
	print(value)

def process_apriori(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	data = kwargs["dag_run"].conf.get("enrichment")["__var"]["apr"]["__var"]
	colItem = data["colItem"]
	collection = data["collection"]
	collectionOut = data["collectionOut"]
	custField = data["custField"]
	database = data["database"]
	dbItem = data["dbItem"]
	find = data["find"]
	itemField = data["itemField"]
	supportCount = data["supportCount"]
	output = algorithm_client_pulse.process_apriori(p_auth, colItem, collection, collectionOut, custField, database, dbItem, find, itemField, supportCount)
	print(output)

def preprocess_generate_forecast(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	value = kwargs["dag_run"].conf.get("prepare")["__var"]["fore"]
	print(value)

def generate_forecast(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	data = kwargs["dag_run"].conf.get("enrichment")["__var"]["fore"]["__var"]
	attribute = data["attribute"]
	collection = data["collection"]
	collectionOut = data["collectionOut"]
	database = data["database"]
	dateattribute = data["dateattribute"]
	find = data["find"]
	historicsteps = data["historicsteps"]
	steps = data["steps"]
	output = algorithm_client_pulse.generate_forecast(p_auth, attribute, collection, collectionOut, database, dateattribute, find, historicsteps, steps)
	print(output)

def preprocess_prediction_enrich(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	value = kwargs["dag_run"].conf.get("prepare")["__var"]["pred"]
	print(value)

def prediction_enrich(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	data = kwargs["dag_run"].conf.get("enrichment")["__var"]["pred"]["__var"]
	attributes = data["attributes"]
	collection = data["collection"]
	limit = data["limit"]
	mongodb = data["mongodb"]
	predictor = data["predictor"]
	predictor_label = data["predictor_label"]
	search = data["search"]
	skip = data["skip"]
	sort = data["sort"]
	output = data_munging_engine.prediction_enrich_fast(p_auth, mongodb, collection, search, sort, predictor, predictor_label, attributes, skip, limit)
	print(output)


from prediction import jwt_access

def read_collections(auth, database):
	output = data_management_engine.get_document_db_collections(auth, database)
	names = []
	for col in output["collection"]:
		names.append(col["name"])
	for name in names:
		print("\t\t{}".format(name))

def read_dbs(auth):
	output = data_management_engine.get_document_db_list(auth)
	names = []
	for db in output["databases"]:
		names.append(db["name"])
	print("DBS:")
	for name in names:
		print("\t{}:".format(name))
		read_collections(auth, name)

def read_files(auth):
	output = worker_file_service.get_files(auth)
	names = []
	for f in output["item"]:
		names.append(f["name"])
	print("Files:")
	for name in names:
		print("\t{}".format(name))