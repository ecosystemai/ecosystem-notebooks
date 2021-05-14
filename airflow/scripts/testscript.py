from prediction import jwt_access
from prediction.apis import data_management_engine
import subprocess

def get_db_list(**kwargs):
	url = kwargs["dag_run"].conf.get("url")
	username = kwargs["dag_run"].conf.get("username")
	password = kwargs["dag_run"].conf.get("password")
	p_auth = jwt_access.Authenticate(url, username, password)
	output = data_management_engine.get_document_db_list(p_auth)
	print(output)