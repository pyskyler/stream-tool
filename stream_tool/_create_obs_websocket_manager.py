from obswebsocket import obsws  # noqa: E402

def create_obs_websocket_manager(website_settings):
    # Connect to websockets
    ws = obsws(website_settings.websocket_host, website_settings.websocket_port, website_settings.websocket_password)
    ws.connect()
    print("Connected to OBS Websockets!\n")
    return ws
