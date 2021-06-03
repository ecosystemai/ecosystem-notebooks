from prediction.apis import data_management_engine
import authenticate

def get_db_list(**kwargs):
	# url = kwargs["dag_run"].conf.get("url")
	# username = kwargs["dag_run"].conf.get("username")
	# password = kwargs["dag_run"].conf.get("password")
	# p_auth = jwt_access.Authenticate(url, username, password)
	p_auth = authenticate.prediction_login(**kwargs)
	output = data_management_engine.get_document_db_list(p_auth)
	print(output)