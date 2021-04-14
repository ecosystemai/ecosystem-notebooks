from runtime.endpoints import data_management_engine as endpoints
from runtime import request_utils

# Data Management Engine
def get_document_db_collections(auth, database):
	ep = endpoints.GET_MONGO_DB_COLLECTIONS
	param_dict = {
		"database": database
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def get_data(auth, database, collection, field, limit, projections, skip):
	ep = endpoints.GET_MONGO_DB_FIND
	param_dict = {
		"database": database, 
		"collection": collection,
		"field": field,
		"limit": limit,
		"projections": projections, 
		"skip": skip
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def get_data_sort(auth, database, collection, field, limit, projections, skip, sort):
	ep = endpoints.GET_MONGO_DB_FIND_SORT
	param_dict = {
		"database": database, 
		"collection": collection,
		"field": field,
		"limit": limit,
		"projections": projections, 
		"skip": skip,
		"sort": sort
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def get_document_db_list(auth, server=None):
	ep = endpoints.GET_MONGO_DB_LIST
	if server == None:
		server = auth.get_server()
	param_dict = {
		"server": server
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta
