from prediction.endpoints import transaction_categorization as endpoints
import prediction.request_utils

def get_transactions(auth, json):
    ep = endpoints.GET_TRANSACTIONS
    resp = request_utils.create(auth, ep, json=json)
    result = resp.json()
    return result

def get_transactions_cat_predicted(auth, json):
    ep = endpoints.GET_TRANSACTIONS_CAT_PREDICTED
    resp = request_utils.create(auth, ep, json=json)
    result = resp.json()
    return result

def get_transactions_processed(auth, count):
    ep = endpoints.GET_TRANSACTIONS_PROCESSED
    param_dict = {"count": count}
    resp = request_utils.create(auth, ep, params=param_dict)
    transactions = resp.json()
    if "items" in transactions:
        transactions = transactions["items"]
    return transactions