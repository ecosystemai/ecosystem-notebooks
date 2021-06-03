from prediction import jwt_access

def prediction_login(**kwargs):
	url = kwargs["dag_run"].conf.get("url")
	username = kwargs["dag_run"].conf.get("username")
	password = kwargs["dag_run"].conf.get("password")
	auth = jwt_access.Authenticate(url, username, password)
	return auth