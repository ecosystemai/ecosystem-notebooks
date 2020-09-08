from runtime.endpoints import restart_controller as endpoints
from runtime import request_utils

# Restart the server
def restart(auth):
    ep = endpoints.RESTART
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta

# Restart using actuator
def restart_app(auth):
    ep = endpoints.RESTART_APP
    resp = request_utils.create(auth, ep)
    meta = resp.json()
    return meta
