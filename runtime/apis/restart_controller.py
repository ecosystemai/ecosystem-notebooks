from endpoints import restart_controller as endpoints
import request_utils

def restart(auth):
    ep = endpoints.RESTART
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

def restart_app(auth):
    ep = endpoints.RESTART_APP
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta
