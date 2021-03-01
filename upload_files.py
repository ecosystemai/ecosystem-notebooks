from prediction.apis import data_management_engine
import ecosystem_scoring_dash as sd
from prediction import jwt_access

# def upload_file_runtime(auth, path, target_path):
# 	worker_utilities.upload_file(sauth, path, target_path)

# def upload_import_runtime(auth, path, target_path, database, feature_store, feature_store_file):
# 	upload_file_runtime(auth, path, target_path)
# 	worker_utilities.file_database_import(auth, database, feature_store, feature_store_file)

# def upload_file_pred(auth, path, target_path):
# 	worker_file_service.upload_file(auth, path, "/data/" +  target_path)

# def upload_import_pred(auth, path, target_path, database, feature_store, feature_store_file):
# 	upload_file_pred(auth, path, target_path)
# 	data_management_engine.csv_import(auth, database, feature_store, feature_store_file)

pred_url = "http://127.0.0.1:4000/api"
pred_username = "admin@ecosystem.ai"
pred_pass = "password"

auth = jwt_access.Authenticate(pred_url, pred_username, pred_pass)

# destinations = "listOfDestinations.txt"
sd.upload_file_pred(auth, "C:/Users/Ramsay/Documents/GitHub/data/fnb/data/listOfDestinations.txt", "/")


sd.upload_file_pred(auth, "enrich_for_runtime.py", "/")
# sd.upload_import_pred(auth, "test_customer.csv", "/", "fnb", "customers_upload", "test_customer.csv")
# sd.upload_import_pred(auth, "test_transactions.csv", "/", "fnb", "transactions_upload", "test_transactions.csv")
# sd.upload_import_pred(auth, "test_CTO.csv", "/", "fnb", "CTO_upload", "test_CTO.csv")

# results = data_management_engine.get_data(auth, "fnb", "customers_upload", "{}", 1000000, "{}", 0)
# for doc in results:
# 	print(doc)


# sd.upload_file_pred(auth, "fnb/data/listOfDestinations.txt", "/")

# db_name = "fnb"

# proc_tx_data = "transactions_test"
# sd.upload_import_pred(auth, "fnb/data/transactions.csv", "/", db_name, proc_tx_data, "transactions.csv")

# proc_customer_data = "customer_test"
# sd.upload_import_pred(auth, "fnb/data/customer.csv", "/", db_name, proc_customer_data, "customer.csv")

# cto_data = "cto_test"
# sd.upload_import_pred(auth, "fnb/data/CTO.csv", "/", db_name, cto_data, "CTO.csv")

# sample_tx_data_rollup = "transactions_rollup_test"
# sample_tx_data_rollup_norm = "transactions_rollup_normalise_test"