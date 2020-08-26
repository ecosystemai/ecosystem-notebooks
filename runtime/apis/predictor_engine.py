from endpoints import predictor_engine as endpoints
import request_utils

def get_estore_recommendations(auth, campaign_id, channel_name, headers, msisdn, number_of_offers, params, payment_method, sub_campaign_id, user_id):
    ep = endpoints.GET_OFFER_RECOMMENDATIONS
    param_dict = {
        "campaign_id": campaign_id, 
        "channel_name": channel_name,
        "headers": headers,
        "msisdn": msisdn,
        "number_of_offers": number_of_offers,
        "params": params,
        "payment_method": payment_method,
        "sub_campaign_id": sub_campaign_id,
        "user_id": user_id
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def put_estore_recommendations(auth, document, headers):
    ep = endpoints.PUT_ESTORE_RECOMMENDATIONS
    param_dict = {
        "document": document, 
        "headers": headers
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def get_estore_recommender_non_gsm(auth, campaign_id, channel_name, headers, msisdn, number_of_offers, params, payment_method, sub_campaign_id, user_id):
    ep = endpoints.GET_ESTORE_RECOMMENDER_NON_GSM
    param_dict = {
        "campaign_id": campaign_id, 
        "channel_name": channel_name,
        "headers": headers,
        "msisdn": msisdn,
        "number_of_offers": number_of_offers,
        "params": params,
        "payment_method": payment_method,
        "sub_campaign_id": sub_campaign_id,
        "user_id": user_id
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def put_estore_recommender_non_gsm(auth, document, headers):
    ep = endpoints.PUT_ESTORE_RECOMMENDER_NON_GSM
    param_dict = {
        "document": document, 
        "headers": headers
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

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

def gift_recommendations(auth, document):
    ep = endpoints.GIFT_RECOMMENDATIONS
    param_dict = {
        "document": document
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def gift_recommendations_free(auth, campaign_id, channel_name, headers, msisdn, number_of_offers, params, payment_method, sub_campaign_id, transaction_id, user_id):
    ep = endpoints.GIFT_RECOMMENDATIONS_FREE
    param_dict = {
        "campaign_id": campaign_id,
        "channel_name": channel_name,
        "headers": headers,
        "msisdn": msisdn,
        "number_of_offers": number_of_offers,
        "params": params,
        "payment_method": payment_method,
        "sub_campaign_id": sub_campaign_id,
        "transaction_id": transaction_id,
        "user_id": user_id
    }
    resp = request_utils.create(auth, ep, params=param_dict)
    meta = resp.json()
    return meta

def gift_recommendations_purchased(auth, campaign_id, channel_name, headers, msisdn, number_of_offers, params, payment_method, sub_campaign_id, transaction_id, user_id):
    ep = endpoints.GIFT_RECOMMENDATIONS_PURCHASED
    param_dict = {
        "campaign_id": campaign_id,
        "channel_name": channel_name,
        "headers": headers,
        "msisdn": msisdn,
        "number_of_offers": number_of_offers,
        "params": params,
        "payment_method": payment_method,
        "sub_campaign_id": sub_campaign_id,
        "transaction_id": transaction_id,
        "user_id": user_id
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