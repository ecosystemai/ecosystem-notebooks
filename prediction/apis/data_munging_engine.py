from prediction.endpoints import data_munging_engine as endpoints
from prediction import request_utils
from prediction.apis import quickflat as qf

def concat_columns2(auth, database, collection, attribute, separator):
    ep = endpoints.CONCAT_COLUMNS2
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "attribute": attribute,
        "separator": separator
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def enrich_date2(auth, database, collection, attribute, find):
    ep = endpoints.DATE_ENRICH2
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "attribute": attribute,
        "find": find
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def auto_normalize_all(auth, database, collection, fields, find, normalized_high, normalized_low):
    ep = endpoints.AUTO_NORMALIZE_ALL
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "fields": fields,
        "find": find,
        "normalizedHigh": normalized_high,
        "normalizedLow": normalized_low
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def concat_columns(auth, databasename, collection, attribute):
    ep = endpoints.CONCAT_COLUMNS
    param_dict = {"mongodb": databasename, "collection": collection, "attribute": attribute}
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def enrich_date(auth, database, collection, attribute):
    ep = endpoints.DATE_ENRICH
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "attribute": attribute
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def enum_convert(auth, database, collection, attribute):
    ep = endpoints.ENUM_CONVERT
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "attribute": attribute
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def fill_zeros(auth, database, collection, attribute):
    ep = endpoints.FILL_ZEROES
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "attribute": attribute
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def foreign_key_aggregator(auth, database, collection, attribute, search, mongodbf, collectionf, attributef, fields):
    ep = endpoints.FOREIGN_KEY_AGGREGATOR
    param_dict = {
        "mongodb": database,
        "collection": collection,
        "attribute": attribute,
        "search": search,
        "mongodbf": mongodbf,
        "collectionf": collectionf,
        "attributef": attributef,
        "fields": fields
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def foreign_key_lookup(auth, database, collection, attribute, search, mongodbf, collectionf, attributef, fields):
    ep = endpoints.FOREIGN_KEY_LOOKUP
    param_dict = {
        "mongodb": database,
        "collection": collection,
        "attribute": attribute,
        "search": search,
        "mongodbf": mongodbf,
        "collectionf": collectionf,
        "attributef": attributef,
        "fields": fields
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def enrich_fragments(auth, database, collection, attribute, strings):
    ep = endpoints.FRAGMENT_ENRICH
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "attribute": attribute,
        "stringOnly": strings
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def enrich_fragments2(auth, database, collection, attribute, strings, find):
    ep = endpoints.FRAGMENT_ENRICH2
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "attribute": attribute,
        "stringOnly": strings,
        "find": find
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def generate_features(auth, database, collection, featureset, categoryfield, datefield, numfield, groupby, find):
    ep = endpoints.GENERATE_FEATURES
    param_dict = {"database": database, "collection": collection, "featureset":featureset, "categoryfield":categoryfield, "datefield":datefield, "numfield":numfield, "groupby":groupby, "find":find}
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def generate_features_normalize(auth, database, collection, find, inplace, normalized_high, normalized_low, numfields):
    ep = endpoints.GENERATE_FEATURES_NORMALIZE
    param_dict = {"database": database, "collection": collection, "find":find, "inPlace": inplace, "normalizedHigh": normalized_high, "normalizedLow": normalized_low, "numfields": numfields}
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def get_categories(auth, database, collection, categoryfield, find, total):
    ep = endpoints.GET_CATEGORIES
    param_dict = {"database": database, "collection":collection, "categoryfield":categoryfield, "total": total, "find": find}
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def get_categories_ratio(auth, database, collection, categoryfield, find, total):
    ep = endpoints.GET_CATEGORIES_RATIOS
    param_dict = {"database": database, "collection":collection, "categoryfield":categoryfield, "total": total, "find": find}
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def enrich_location(auth, database, collection, attribute):
    ep = endpoints.LOCATION_ENRICH
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "attribute": attribute
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def enrich_mcc(auth, database, collection, attribute, find):
    ep = endpoints.MCC_ENRICH
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "attribute": attribute,
        "find": find
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def munge_transactions(auth, munging_step, project_id):
    ep = endpoints.MUNGE_TRANSACTIONS
    param_dict = {
        "munging_step": munging_step, 
        "project_id": project_id
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def munge_transactions_aggregate(auth, munging_step, project_id):
    ep = endpoints.MUNGE_TRANSACTIONS_AGGREGATE
    param_dict = {
        "munging_step": munging_step, 
        "project_id": project_id
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

# TODO: Should Add regular and Post of fast endpoints.
def enrich_predictor(auth, database, collection, search, sort, predictor, predictor_label, attributes, skip, limit):
    ep = endpoints.PREDICTION_ENRICH_FAST_GET
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "search": search,
        "sort": sort,
        "predictor": predictor,
        "predictor_label": predictor_label,
        "attributes": attributes,
        "skip": skip,
        "limit": limit
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def enrich_sic(auth, database, collection, attribute, find):
    ep = endpoints.SIC_ENRICH
    param_dict = {
        "mongodb": database, 
        "collection": collection,
        "attribute": attribute,
        "find": find
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def quickflat(config):
	quick_flat = qf.QuickFlat(config)
	quick_flat.flatten()