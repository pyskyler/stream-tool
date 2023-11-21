from obswebsocket import obsws  # noqa: E402
from . import Websockets_Auth


def create_obs_websocket_manager():
    # Connect to websockets
    ws = obsws(Websockets_Auth.websocket_host, Websockets_Auth.websocket_port, Websockets_Auth.websocket_password)
    ws.connect()
    print("Connected to OBS Websockets!\n")
    return ws
