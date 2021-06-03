from prediction.endpoints import prediction_engine as endpoints
from prediction import request_utils

def delete_analysis(auth, analysis_id):
	ep = endpoints.DELETE_ANALYSIS
	resp = request_utils.create(auth, ep, ep_arg=analysis_id)
	result = resp.json()
	return result

def delete_model(auth, model_id):
	ep = endpoints.DELETE_MODEL
	resp = request_utils.create(auth, ep, ep_arg=model_id)
	result = resp.json()
	return result

def delete_prediction(auth, prediction_id):
	ep = endpoints.DELETE_PREDICTION
	resp = request_utils.create(auth, ep, ep_arg=prediction_id)
	result = resp.json()
	return result

def delete_prediction_project(auth, prediction_project_id):
	ep = endpoints.DELETE_PREDICTION_PROJECT
	resp = request_utils.create(auth, ep, ep_arg=prediction_project_id)
	result = resp.json()
	return result

def delete_user_deployments(auth, user_deployments_id):
	ep = endpoints.DELETE_USER_DEPLOYMENTS
	resp = request_utils.create(auth, ep, ep_arg=user_deployments_id)
	result = resp.json()
	return result

def delete_userframe(auth, frame_id):
	ep = endpoints.DELETE_USER_FRAME
	param_dict = {"frame_id": frame_id}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def deploy_predictor(auth, json):
	ep = endpoints.DEPLOY_PREDICTOR
	resp = request_utils.create(auth, ep, json=json)
	response = resp.json()
	return response

def get_analysis_result(auth, analysis_id):
	ep = endpoints.GET_ANALYSIS_RESULT
	param_dict = {"analysis_id": analysis_id}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def get_analysis_results(auth):
	ep = endpoints.GET_ANALYSIS_RESULTS
	param_dict = {"user": ep.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict)
	results = resp.json()
	if "item" in results:
		results = results["item"]
	return results

def get_prediction(auth, predict_id):
	ep = endpoints.GET_PREDICTION
	param_dict = {"predict_id": predict_id}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def get_prediction_project(auth, project_id):
	ep = endpoints.GET_PREDICTION
	param_dict = {"project_id": project_id}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

# TODO: all these ep.get_username() call might need to be replaced with arguments that check if a  value is passed first
def get_prediction_projects(auth):
	ep = endpoints.GET_PREDICTION_PROJECTS
	param_dict = {"user": ep.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict)
	projects = resp.json()
	if "item" in projects:
		projects = projects["item"]
	return projects

def get_user_deployment(auth, user_deployments):
	ep = endpoints.GET_USER_DEPLOYMENT
	param_dict = {"user_deployments": user_deployments}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def get_user_deployments(auth):
	ep = endpoints.GET_USER_DEPLOYMENTS
	param_dict = {"user": ep.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict)
	deployments = resp.json()
	if "item" in deployments:
		deployments = deployments["item"]
	return deployments

def get_user_featurestores(auth):
	ep = endpoints.GET_USER_FEATURE_STORES
	param_dict = {"user": ep.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict)
	featurestores = resp.json()
	if "item" in featurestores:
		featurestores = featurestores["item"]
	return featurestores

def get_user_files(auth):
	ep = endpoints.GET_USER_FILES
	param_dict = {"user": ep.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict)
	files = resp.json()
	if "item" in files:
		files = files["item"]
	return files

def get_featurestores(auth):
	ep = endpoints.GET_USER_FRAMES
	param_dict = {"user": auth.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict)
	frames = resp.json()
	if "item" in frames:
		frames = frames["item"]
	return frames

def get_featurestore(auth, frame_id):
	ep = endpoints.GET_USER_FRAME
	param_dict = {"frame_id": frame_id}
	resp = request_utils.create(auth, ep, params=param_dict)
	userframe = resp.json()
	return userframe

def get_uframe(auth, frame_id):
	ep = endpoints.GET_USER_FRAME
	param_dict = {"frame_id": frame_id}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp
	return result

def get_user_model(auth, model_identity):
	ep = endpoints.GET_USER_MODEL
	param_dict = {"model_identity": model_identity}
	resp = request_utils.create(auth, ep, params=param_dict)
	result = resp.json()
	return result

def get_user_models(auth):
	ep = endpoints.GET_USER_MODELS
	param_dict = {"user": ep.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict)
	models = resp.json()
	if "item" in models:
		models = models["item"]
	return models

def get_user_predictions(auth):
	ep = endpoints.GET_USER_PREDICTIONS
	param_dict = {"user": ep.get_username()}
	resp = request_utils.create(auth, ep, params=param_dict)
	predictions = resp.json()
	if "item" in predictions:
		predictions = predictions["item"]
	return predictions

def save_analysis(auth, analysis):
	ep = endpoints.SAVE_ANALYSIS
	resp = request_utils.create(auth, ep, json=analysis)
	response = resp.json()
	return response

def save_model(auth, model):
	ep = endpoints.SAVE_MODEL
	resp = request_utils.create(auth, ep, json=model)
	response = resp.json()
	return response

def save_prediction(auth, prediction):
	ep = endpoints.SAVE_PREDICTION
	resp = request_utils.create(auth, ep, json=prediction)
	response = resp.json()
	return response

def save_analysis(auth, analysis):
	ep = endpoints.SAVE_ANALYSIS
	resp = request_utils.create(auth, ep, json=analysis)
	response = resp.json()
	return response

def save_prediction_project(auth, prediction_project):
	ep = endpoints.SAVE_PREDICTION_PROJECT
	resp = request_utils.create(auth, ep, json=prediction_project)
	response = resp.json()
	return response

def save_user_deployments(auth, user_deployments):
	ep = endpoints.SAVE_USER_DEPLOYMENTS
	resp = request_utils.create(auth, ep, json=user_deployments)
	response = resp.json()
	return response

def save_user_frame(auth, user_frame):
	ep = endpoints.SAVE_USER_FRAME
	resp = request_utils.create(auth, ep, json=user_frame)
	response = resp.json()
	return response

def test_model(auth, value):
	ep = endpoints.TEST_PREDICTOR
	param_dict = {"value": value}
	resp = request_utils.create(auth, ep, params=param_dict)
	response = resp.json()
	return response
