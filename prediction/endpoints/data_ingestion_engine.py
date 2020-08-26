# Data Ingestion Engine
ADD_META_DOCUMENTS = {
	"type": "post",
	"endpoint": "/addMetaDocuments",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DELETE_INGEST_META = {
	"type": "post",
	"endpoint": "/deleteIngestMeta",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

GET_DATABASES_META = {
	"type": "get",
	"endpoint": "/getDatabasesMeta",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_DATABASE_TABLE_COLUMN_META = {
	"type": "get",
	"endpoint": "/getDatabaseTableColumnMeta",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_DATABASE_TABLE_COLUMNS_META = {
	"type": "get",
	"endpoint": "/getDatabaseTableColumnsMeta",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_DATABASE_TABLES_META = {
	"type": "get",
	"endpoint": "/getDatabaseTablesMeta",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_INGEST_META = {
	"type": "get",
	"endpoint": "/getIngestMeta",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_INGEST_METAS = {
	"type": "get",
	"endpoint": "/getIngestMetas",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
SAVE_DATABASE_TABLE_COLUMN_META = {
	"type": "post",
	"endpoint": "/saveDatabaseTableColumnMeta",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
SAVE_INGEST_META = {
	"type": "post",
	"endpoint": "/saveIngestMeta",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}