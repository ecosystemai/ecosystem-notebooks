UPDATE_PROPERTIES = {
	"type": "post",
	"endpoint": "/updateProperties",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

UPLOAD_FILE = {
	"type": "post",
	"endpoint": "/upload",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

GET_FILE_TAIL = {
	"type": "get",
	"endpoint": "/getFileTail",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}