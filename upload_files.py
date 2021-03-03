from prediction.apis import data_management_engine
import ecosystem_scoring_dash as sd
from prediction import jwt_access

pred_url = "http://127.0.0.1:3001/api"
pred_username = "admin@ecosystem.ai"
pred_pass = "password"

auth = jwt_access.Authenticate(pred_url, pred_username, pred_pass)


sd.upload_file_pred(auth, "C:/Users/Ramsay/Documents/GitHub/data/fnb/data/listOfDestinations.txt", "/")
sd.upload_file_pred(auth, "enrich_for_runtime.py", "/")
