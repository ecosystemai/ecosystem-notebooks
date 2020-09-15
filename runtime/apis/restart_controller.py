from runtime.endpoints import restart_controller as endpoints
from runtime import request_utils

def restart(auth):
# Restart the server
    ep = endpoints.RESTART
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

def restart_app(auth):
# Restart using actuator
    ep = endpoints.RESTART_APP
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta
