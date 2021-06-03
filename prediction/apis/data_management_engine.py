from prediction.endpoints import data_management_engine as endpoints
from prediction import request_utils

# Data Management Engine
def get_document_db_aggregate2(auth, database, collection, aggregate, field, limit, projections, skip, sort):
	ep = endpoints.GET_MONGO_DB_AGGREGATE2
	param_dict = {
		"database": database, 
		"collection": collection,
		"aggregate": aggregate,
		"field": field,
		"limit": limit,
		"projections": projections,
		"skip": skip,
		"sort": sort
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def add_document_collection(auth, database, collection):
	ep = endpoints.ADD_MONGO_COLLECTION
	param_dict = {
		"database": database, 
		"collection": collection
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def add_document_database(auth, database):
	ep = endpoints.ADD_MONGO_DATABASE
	param_dict = {
		"database": database
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def add_documents(auth, json, info=True):
	ep = endpoints.ADD_MONGO_DOCUMENTS
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def csv_file_to_json(auth, csv_file, json_file):
	ep = endpoints.CSV_FILE_TO_JSON
	param_dict = {
		"csv_file": csv_file,
		"json_file": json_file
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def csv_import(auth, database, collection, csv_file):
	ep = endpoints.CSV_FILE_TO_MONGO_DB_IMPORT
	param_dict = {
		"database": database, 
		"collection": collection,
		"csv_file": csv_file
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def csv_import2(auth, database, collection, csv_file, headerline, import_type):
	ep = endpoints.CSV_FILE_TO_MONGO_DB_IMPORT2
	param_dict = {
		"database": database, 
		"collection": collection,
		"csv_file": csv_file,
		"headerline": headerline,
		"type": import_type

	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def delete_all_documents(auth, doc_json):
	ep = endpoints.DELETE_ALL_MONGO_DOCUMENTS
	resp = request_utils.create(auth, ep, json=doc_json)
	response = resp.json()
	return response

def delete_documents(auth, doc_json):
	ep = endpoints.DELETE_MONGO_DOCUMENTS
	resp = request_utils.create(auth, ep, json=doc_json)
	response = resp.json()
	return response

def drop_document_collection(auth, database, collection):
	ep = endpoints.DROP_MONGO_COLLECTION
	param_dict = {
		"database": database, 
		"collection": collection
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def drop_document_collection_index(auth, database, collection, index):
	ep = endpoints.DROP_MONGO_COLLECTION_INDEX
	param_dict = {
		"database": database, 
		"collection": collection,
		"index": index
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def drop_document_database(auth, database):
	ep = endpoints.DROP_MONGO_DATABASE
	param_dict = {
		"database": database
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def dump_document_database(auth, database, collection, folder, option):
	ep = endpoints.DUMP_MONGO_DATABASE
	param_dict = {
		"database": database,
		"collection": collection,
		"folder": folder,
		"option": option
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def execute_document_db_script(auth, param):
	ep = endpoints.EXECUTE_MONGO_DB_SCRIPT
	param_dict = {
		"param": param
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def export_documents(auth, filename, filetype, database, collection, field, sort, projection, limit):
	ep = endpoints.EXPORT_MONGO_DOCUMENTS 
	param_dict = {
		"file_name": filename,
		"file_type": filetype,
		"database": database, 
		"collection": collection,
		"field": field,
		"sort": sort,
		"projection": projection,
		"limit": limit
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def get_document_collection_indexes(auth, database, collection):
	ep = endpoints.GET_MONGO_COLLECTION_INDEXES
	param_dict = {
		"database": database, 
		"collection": collection
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def get_data_aggregate(auth, database, collection, field, projections, aggregate, sort):
	ep = endpoints.GET_MONGO_DB_AGGREGATE 
	param_dict = {
		"database": database, 
		"collection": collection,
		"field": field,
		"projections": projections,
		"aggregate": aggregate,
		"sort": sort
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta
	
def get_document_db_collections(auth, database):
	ep = endpoints.GET_MONGO_DB_COLLECTIONS
	param_dict = {
		"database": database
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def get_document_db_collection_stats(auth, database, collection):
	ep = endpoints.GET_MONGO_DB_COLLECTION_STATS
	param_dict = {
		"database": database, 
		"collection": collection
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
	
def get_document_db_find_labels(auth, database, collection, field, projections, skip):
	ep = endpoints.GET_MONGO_DB_FIND_LABELS
	param_dict = {
		"database": database, 
		"collection": collection,
		"field": field,
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

def get_documents_lables(auth, database, collection):
	ep = endpoints.GET_MONGO_DOCUMENT_LABLES
	param_dict = {
		"database": database,
		"collection": collection
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def import_documents(auth, database, collection, file_name, file_type):
	ep = endpoints.IMPORT_MONGO_DOCUMENTS
	param_dict = {
		"database": database,
		"collection": collection,
		"file_name": file_name,
		"file_type": file_type
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def restore_document_database(auth, database, collection, folder):
	ep = endpoints.GET_MONGO_DOCUMENT_LABLES
	param_dict = {
		"database": database,
		"collection": collection,
		"folder": folder
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

# Data Management Engine: Cassandra
def get_cassandra_sql(auth, sql):
	ep = endpoints.GET_CASSANDRA_SQL
	param_dict = {
		"sql": sql
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

# Data Management Engine: Presto
def create_presto_sql(auth, connection, sql):
	ep = endpoints.CREATE_PRESTO_SQL
	param_dict = {
		"connection": connection,
		"sql": sql
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def get_presto_sql(auth, connection, sql):
	ep = endpoints.GET_PRESTO_SQL
	param_dict = {
		"connection": connection,
		"sql": sql
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result