from prediction.apis import data_management_engine
from prediction.apis import data_munging_engine
from prediction.apis import worker_file_service
from prediction.apis import algorithm_client_pulse
import authenticate

def list_collections(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	database = "nlp_examples"
	output = data_management_engine.get_document_db_collections(p_auth, database)
	print(output)

def read_data(**kwargs):
	p_auth = authenticate.prediction_login(**kwargs)
	database = "nlp_examples"
	collection = "nlp_example_text"
	field = "{}"
	limit = 0
	projections = "{}"
	skip = 0
	output = data_management_engine.get_data(p_auth, database, collection, field, limit, projections, skip)
	print(output)