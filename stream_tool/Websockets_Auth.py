"""Information for connecting to OBS websockets

Attributes
----------
websocket_host: str
    The ip address of the websockets server to communicate with. Set to '127.0.0.1' by default
    which is the local machine address.
websocket_port: int
    The port to connect to on the websockets server. Set to 4455 by default which is the OBS default.
websocket_password: str
    The password to connect to the OBS websockets server. Empty by default

"""

websocket_host = "127.0.0.1"
websocket_port = 4455
websocket_password = ""
