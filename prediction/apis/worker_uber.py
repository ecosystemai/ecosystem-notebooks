from prediction.endpoints import worker_uber as endpoints
from prediction import request_utils

def build_model_ludwig(auth, model_name, model_definition):
	ep = endpoints.BUILD_MODEL_LUDWIG
	param_dict = {
		"model_name": model_name,
		"model_definition": model_definition
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def build_orbit_btvc(auth, input_database, input_collection, output_database, output_collection, response_column, date_column, seasonality, seed, find, params):
	ep = endpoints.BUILD_ORBIT_BTVC
	param_dict = {
		"input_database": input_database,
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"response_column": response_column,
		"date_column": date_column,
		"seasonality": seasonality,
		"seed": seed,
		"find": find,
		"params": params
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def build_orbit_dlt(auth, input_database, input_collection, output_database, output_collection, response_column, date_column, seasonality, seed, find, params):
	ep = endpoints.BUILD_ORBIT_DLT
	param_dict = {
		"input_database": input_database,
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"response_column": response_column,
		"date_column": date_column,
		"seasonality": seasonality,
		"seed": seed,
		"find": find,
		"params": params
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def build_orbit_ets(auth, input_database, input_collection, output_database, output_collection, response_column, date_column, seasonality, seed, find):
	ep = endpoints.BUILD_ORBIT_ETS
	param_dict = {
		"input_database": input_database,
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"response_column": response_column,
		"date_column": date_column,
		"seasonality": seasonality,
		"seed": seed,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def build_orbit_lgt(auth, input_database, input_collection, output_database, output_collection, response_column, date_column, seasonality, seed, find):
	ep = endpoints.BUILD_ORBIT_LGT
	param_dict = {
		"input_database": input_database,
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"response_column": response_column,
		"date_column": date_column,
		"seasonality": seasonality,
		"seed": seed,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta