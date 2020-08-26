from prediction.endpoints import algorithm_client_pulse as endpoints
import prediction.request_utils

def get_timeline(auth, user, limit):
    ep = endpoints.GET_TIMELINE
    param_dict = {
        "user": user, 
        "limit": limit
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def process_basket(auth, dbcust, colcust, searchcust, custfield, dbitem, colitem, itemfield, supportcount):
    ep = endpoints.PROCESS_BASKET
    param_dict = {
        "dbCust": dbcust, 
        "colCust": colcust,
        "searchCust": searchcust,
        "custField": custfield,
        "dbItem": dbitem,
        "colItem": colitem,
        "itemField": itemfield,
        "supportCount": supportcount
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def process_directed_graph(auth, graphMeta, graphParam):
    ep = endpoints.PROCESS_BASKET
    param_dict = {
        "graphMeta": graphMeta, 
        "graphParam": graphParam
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta