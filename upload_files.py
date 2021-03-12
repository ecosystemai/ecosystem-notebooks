from prediction.apis import data_management_engine
from prediction.apis import worker_file_service
import ecosystem_scoring_dash as sd
from prediction import jwt_access

pred_url = "http://demo.ecosystem.ai:3001/api"
# pred_url = "http://127.0.0.1:4000/api"
pred_username = "user@ecosystem.ai"
pred_pass = "password"

auth = jwt_access.Authenticate(pred_url, pred_username, pred_pass)
data_path = worker_file_service.get_property(auth, "user.data")

# sd.upload_file_pred(auth, "C:/Users/Ramsay/Documents/GitHub/data/fnb/data/listOfDestinations.txt", str(data_path))
# sd.upload_file_pred(auth, "enrich_for_runtime.py", str(data_path))
sd.upload_file_pred(auth, "C:/Users/Ramsay/Documents/GitHub/data/fnb/data/listOfDestinations.txt", "/")
sd.upload_file_pred(auth, "enrich_for_runtime.py", "/")