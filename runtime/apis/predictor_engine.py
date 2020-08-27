from runtime.endpoints import predictor_engine as endpoints
from runtime import request_utils

def get_spending_personality(auth, campaign, channel, customer, headers, params, subcampaign, userid):
    ep = endpoints.GET_SPENDING_PERSONALITY
    param_dict = {
        "campaign": campaign, 
        "channel": channel,
        "customer": customer,
        "headers": headers,
        "params": params,
        "subcampaign": subcampaign,
        "userid": userid
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def put_spending_personality(auth, document, headers):
    ep = endpoints.PUT_SPENDING_PERSONALITY
    param_dict = {
        "document": document, 
        "headers": headers
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def model_detail(auth, model):
    ep = endpoints.GIFT_RECOMMENDATIONS_PURCHASED
    param_dict = {
        "model": model
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def get_offer_recommendations(auth, campaign, channel, customer, headers, numberoffers, params, subcampaign, userid):
    ep = endpoints.GET_OFFER_RECOMMENDATIONS
    param_dict = {
        "campaign": campaign, 
        "channel": channel,
        "customer": customer,
        "headers": headers,
        "numberoffers": numberoffers,
        "params": params,
        "subcampaign": subcampaign,
        "userid": userid
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def put_offer_recommendations(auth, document, headers):
    ep = endpoints.PUT_OFFER_RECOMMENDATIONS
    param_dict = {
        "document": document, 
        "headers": headers
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def get_personality_recommender(auth, campaign, channel, customer, headers, numberoffers, params, subcampaign, userid):
    ep = endpoints.GET_PERSONALITY_RECOMMENDER
    param_dict = {
        "campaign": campaign, 
        "channel": channel,
        "customer": customer,
        "headers": headers,
        "numberoffers": numberoffers,
        "params": params,
        "subcampaign": subcampaign,
        "userid": userid
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def put_personality_recommender(auth, document, headers):
    ep = endpoints.PUT_PERSONALITY_RECOMMENDER
    param_dict = {
        "document": document, 
        "headers": headers
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def predictor_response_preload(auth, detail, value):
    ep = endpoints.PREDICTOR_RESPONSE_PRELOAD
    param_dict = {
        "detail": detail, 
        "value": value
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def predictor_response_preload_kafka(auth, detail, value):
    ep = endpoints.PREDICTOR_RESPONSE_PRELOAD_KAFKA
    param_dict = {
        "detail": detail, 
        "value": value
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def refresh(auth, headers):
    ep = endpoints.REFRESH
    param_dict = {
        "headers": headers
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def run_model_mojo(auth, detail, value):
    ep = endpoints.RUN_MODEL_MOJO
    param_dict = {
        "detail": detail, 
        "value": value
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta