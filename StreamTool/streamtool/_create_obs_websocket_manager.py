from obswebsocket import obsws  # noqa: E402
from Websockets_Auth import websocket_host, websocket_port, websocket_password

##########################################################
##########################################################

# import logging
# logging.basicConfig(level=logging.DEBUG)


def create_obs_websocket_manager():
    # Connect to websockets
    ws = obsws(websocket_host, websocket_port, websocket_password)
    ws.connect()
    print("Connected to OBS Websockets!\n")
    return ws
