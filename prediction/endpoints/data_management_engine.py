# Data Management Engine
GET_MONGO_DB_AGGREGATE2 = {
	"type": "get",
	"endpoint": "/2/getMongoDBAggregate",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
ADD_MONGO_COLLECTION = {
	"type": "get",
	"endpoint": "/addMongoCollection",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
ADD_MONGO_DATABASE = {
	"type": "get",
	"endpoint": "/addMongoDatabase",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
ADD_MONGO_DOCUMENTS = {
	"type": "post",
	"endpoint": "/addMongoDocuments",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
CSV_FILE_TO_JSON = {
	"type": "get",
	"endpoint": "/csvFileToJSON",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
CSV_FILE_TO_MONGO_DB_IMPORT = {
	"type": "get",
	"endpoint": "/csvFileToMongoDBImport",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
CSV_FILE_TO_MONGO_DB_IMPORT2 = {
	"type": "get",
	"endpoint": "/csvFileToMongoDBImport2",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DELETE_ALL_MONGO_DOCUMENTS = {
	"type": "post",
	"endpoint": "/deleteAllMongoDocuments",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DELETE_MONGO_DOCUMENTS = {
	"type": "post",
	"endpoint": "/deleteMongoDocuments",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DROP_MONGO_COLLECTION = {
	"type": "get",
	"endpoint": "/dropMongoCollection",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DROP_MONGO_COLLECTION_INDEX = {
	"type": "get",
	"endpoint": "/dropMongoCollectionIndex",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DROP_MONGO_DATABASE = {
	"type": "get",
	"endpoint": "/dropMongoDatabase",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DUMP_MONGO_DATABASE = {
	"type": "get",
	"endpoint": "/dumpMongoDatabase",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
EXECUTE_MONGO_DB_SCRIPT = {
	"type": "get",
	"endpoint": "/executeMongoDBScript",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
EXPORT_MONGO_DOCUMENTS = {
	"type": "get",
	"endpoint": "/exportMongoDocuments",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_COLLECTION_INDEXES = {
	"type": "get",
	"endpoint": "/getMongoCollectionIndexes",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_AGGREGATE = {
	"type": "get",
	"endpoint": "/getMongoDBAggregate",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_COLLECTIONS = {
	"type": "get",
	"endpoint": "/getMongoDBCollections",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_COLLECTION_STATS = {
	"type": "get",
	"endpoint": "/getMongoDBCollectionStats",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_FIND = {
	"type": "get",
	"endpoint": "/getMongoDBFind",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_FIND_LABELS = {
	"type": "get",
	"endpoint": "/getMongoDBFindLabels",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_FIND_SORT = {
	"type": "get",
	"endpoint": "/getMongoDBFindSort",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DB_LIST = {
	"type": "get",
	"endpoint": "/getMongoDBList",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_MONGO_DOCUMENT_LABLES = {
	"type": "get",
	"endpoint": "/getMongoDocumentsLabels",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
IMPORT_MONGO_DOCUMENTS = {
	"type": "get",
	"endpoint": "/importMongoDocuments",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
RESTORE_MONGO_DATABASE = {
	"type": "get",
	"endpoint": "/restoreMongoDatabase",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

# Data Management Engine: Cassandra
GET_CASSANDRA_SQL = {
	"type": "get",
	"endpoint": "/getCassandraSQL",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}

# Data Management Engine: Presto
CREATE_PRESTO_SQL = {
	"type": "get",
	"endpoint": "/createPrestoSQL",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}
GET_PRESTO_SQL = {
	"type": "get",
	"endpoint": "/getPrestoSQL",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}