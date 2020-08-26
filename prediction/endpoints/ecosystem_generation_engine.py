# Ecosystem Generation Engine
GENERATE_BUILD = {
	"type": "post",
	"endpoint": "/generateBuild",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GENERATE_PROPERTIES = {
	"type": "post",
	"endpoint": "/generateProperties",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_BUILD = {
	"type": "get",
	"endpoint": "/getBuild",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
PROCESS_BUILD = {
	"type": "post",
	"endpoint": "/processBuild",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}