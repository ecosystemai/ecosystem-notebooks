# Prediction Engine
DELETE_ANALYSIS = {
	"type": "delete",
	"endpoint": "/deleteAnalysis/",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}",
	"target": True
}
DELETE_MODEL = {
	"type": "delete",
	"endpoint": "/deleteModel/",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}",
	"target": True
}
DELETE_PREDICTION = {
	"type": "delete",
	"endpoint": "/deletePrediction/",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}",
	"target": True
}
DELETE_PREDICTION_PROJECT = {
	"type": "delete",
	"endpoint": "/deletePredictionProject/",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}",
	"target": True
}
DELETE_USER_DEPLOYMENTS = {
	"type": "delete",
	"endpoint": "/deleteUserDeployments/",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}",
	"target": True
}
DELETE_USER_FRAME = {
	"type": "get",
	"endpoint": "/deleteUserFrame",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DEPLOY_PREDICTOR = {
	"type": "post",
	"endpoint": "/deployPredictor",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_ANALYSIS_RESULT = {
	"type": "get",
	"endpoint": "/getAnalysisResult",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_ANALYSIS_RESULTS = {
	"type": "get",
	"endpoint": "/getAnalysisResults",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_PREDICTION = {
	"type": "get",
	"endpoint": "/getPrediction",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_PREDICTION_PROJECT = {
	"type": "get",
	"endpoint": "/getPredictionProject",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_PREDICTION_PROJECTS = {
	"type": "get",
	"endpoint": "/getPredictionProjects",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_USER_DEPLOYMENT = {
	"type": "get",
	"endpoint": "/getUserDeployment",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_USER_DEPLOYMENTS = {
	"type": "get",
	"endpoint": "/getUserDeployments",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_USER_FEATURE_STORES = {
	"type": "get",
	"endpoint": "/getUserFeatureStores",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_USER_FILES = {
	"type": "get",
	"endpoint": "/getUserFiles",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_USER_FRAME = {
	"type": "get",
	"endpoint": "/getUserFrame",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_USER_FRAMES = {
	"type": "get",
	"endpoint": "/getUserFrames",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_USER_MODEL = {
	"type": "get",
	"endpoint": "/getUserModel",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_USER_MODELS = {
	"type": "get",
	"endpoint": "/getUserModels",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_USER_PREDICTIONS = {
	"type": "get",
	"endpoint": "/getUserPredictions",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
SAVE_ANALYSIS = {
	"type": "post",
	"endpoint": "/saveAnalysis",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
SAVE_MODEL = {
	"type": "post",
	"endpoint": "/saveModel",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
SAVE_PREDICTION = {
	"type": "post",
	"endpoint": "/savePrediction",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
SAVE_PREDICTION_PROJECT = {
	"type": "post",
	"endpoint": "/savePredictionProject",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
SAVE_USER_DEPLOYMENTS = {
	"type": "post",
	"endpoint": "/saveUserDeployments",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
SAVE_USER_FRAME = {
	"type": "post",
	"endpoint": "/saveUserFrame",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
TEST_PREDICTOR = {
	"type": "get",
	"endpoint": "/testPredictor",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}