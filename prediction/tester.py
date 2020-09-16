from prediction import jwt_access

url = "https://server.ecosystem.ai:3001/api"
username = "user@ecosystem.ai"
password = "12345"
auth = jwt_access.Authenticate(url, username, password)

from prediction.apis import data_management_engine

db_name = "multivariate_testcase"
col_name = "pollution"
result = data_management_engine.get_data(auth, db_name, col_name, {}, 5, {}, 1)
print(result)