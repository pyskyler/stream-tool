import random

from obswebsocket import obsws, requests, events  # noqa: E402
from Websockets_Auth import websocket_host, websocket_port, websocket_password

# import logging
# logging.basicConfig(level=logging.DEBUG)


class OBSWebsocketsManager:
    ws = None

    # define enums
    PLAY_INPUT = "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY"
    STOP_INPUT = "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_STOP"
    PAUSE_INPUT = "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE"

    PLAYING = "OBS_MEDIA_STATE_PLAYING"
    PAUSED = "OBS_MEDIA_STATE_PAUSED"

    def __init__(self):
        # Connect to websockets
        self.ws = obsws(websocket_host, websocket_port, websocket_password)
        self.ws.connect()
        print("Connected to OBS Websockets!\n")
        self.current_playing_song = None

    def disconnect(self):
        self.ws.disconnect()

    # Set the current scene
    def set_scene(self, new_scene):
        self.ws.call(requests.SetCurrentProgramScene(sceneName=new_scene))

    # Set the visibility of any source's filters
    def set_filter_visibility(self, source_name, filter_name, filter_enabled=True):
        self.ws.call(requests.SetSourceFilterEnabled(
            sourceName=source_name, filterName=filter_name, filterEnabled=filter_enabled))

    # Set the visibility of any source
    def set_source_visibility(self, scene_name, source_name, source_visible=True):
        response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
        my_item_id = response.datain['sceneItemId']
        self.ws.call(requests.SetSceneItemEnabled(
            sceneName=scene_name, sceneItemId=my_item_id, sceneItemEnabled=source_visible))

    # Returns the current text of a text source
    def get_text(self, source_name):
        response = self.ws.call(requests.GetInputSettings(inputName=source_name))
        return response.datain["inputSettings"]["text"]

    # Returns the text of a text source
    def set_text(self, source_name, new_text):
        self.ws.call(requests.SetInputSettings(inputName=source_name, inputSettings={'text': new_text}))

    def get_source_transform(self, scene_name, source_name):
        response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
        my_item_id = response.datain['sceneItemId']
        response = self.ws.call(requests.GetSceneItemTransform(sceneName=scene_name, sceneItemId=my_item_id))
        transform = {"positionX": response.datain["sceneItemTransform"]["positionX"],
                     "positionY": response.datain["sceneItemTransform"]["positionY"],
                     "scaleX": response.datain["sceneItemTransform"]["scaleX"],
                     "scaleY": response.datain["sceneItemTransform"]["scaleY"],
                     "cropTop": response.datain["sceneItemTransform"]["cropTop"],
                     "cropBottom": response.datain["sceneItemTransform"]["cropBottom"],
                     "cropLeft": response.datain["sceneItemTransform"]["cropLeft"],
                     "cropRight": response.datain["sceneItemTransform"]["cropRight"],
                     "rotation": response.datain["sceneItemTransform"]["rotation"]}
        return transform

    # The transform should be a dictionary containing any of the following keys with corresponding values
    # positionX, positionY, scaleX, scaleY, cropTop, cropBottom, cropLeft, cropRight, rotation
    # e.g. {"scaleX" = 2, "scaleY" = 2.5}
    # Note: there are other transform settings, like height, width, sourceHeight, sourceWidth, alignment, etc., but
    # these feel like the main useful ones.
    # Use get_source_transform to see the full list
    def set_source_transform(self, scene_name, source_name, new_transform):
        response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
        my_item_id = response.datain['sceneItemId']
        self.ws.call(requests.SetSceneItemTransform(
            sceneName=scene_name, sceneItemId=my_item_id, sceneItemTransform=new_transform))

    # Note: an input, like a text box, is a type of source. This will get *input-specific settings*, not the broader
    # source settings like transform and scale
    # For a text source, this will return settings like its font, color, etc
    def get_input_settings(self, input_name):
        return self.ws.call(requests.GetInputSettings(inputName=input_name))

    # set the input settings, input settings takes an object that can be retrieved from the above function
    def set_input_settings(self, input_name, input_settings):
        self.ws.call(requests.SetInputSettings(inputName=input_name, inputSettings=input_settings))

    # Get list of all the input types
    def get_input_kind_list(self):
        return self.ws.call(requests.GetInputKindList())

    # Get list of all items in a certain scene
    def get_scene_items(self, scene_name):
        return self.ws.call(requests.GetSceneItemList(sceneName=scene_name))

    def transition_to_scene(self, scene_name, transition_name):
        self.ws.call(requests.SetCurrentPreviewScene(sceneName=scene_name))
        self.ws.call(requests.SetCurrentSceneTransition(transitionName=transition_name))
        self.ws.call(requests.TriggerStudioModeTransition())

    def get_current_program_scene(self):
        response = self.ws.call(requests.GetCurrentProgramScene())
        current_scene = response.datain['currentProgramSceneName']
        return current_scene

    def pause_audio(self, input_name):
        self.ws.call(requests.TriggerMediaInputAction(inputName=input_name, mediaAction=self.PAUSE_INPUT))

    def stop_audio(self, input_name):
        self.ws.call(requests.TriggerMediaInputAction(inputName=input_name, mediaAction=self.STOP_INPUT))

    # File to play is optional
    def play_audio(self, input_name, file_name=None):
        if file_name is not None:
            response = self.get_input_settings(input_name)

            input_settings = response.datain['inputSettings']  # Change file Name to be the value passed into func
            input_settings['local_file'] = file_name
            self.set_input_settings(input_name, input_settings)

        self.ws.call(requests.TriggerMediaInputAction(inputName=input_name, mediaAction=self.PLAY_INPUT))

    def play_playlist(self, playlist, input_name):

        # stop all events listened to so this one will control music
        self.ws.eventmanager.functions = []

        def play_next_song(output_data):
            if output_data.datain['inputName'] == 'Music':
                next_song = playlist.songs_list[
                    random.randint(0, (len(playlist.songs_list)-1))]  # pick a song

                while next_song == self.current_playing_song:  # if the current song is the same as next pick a new one
                    next_song = playlist.songs_list[
                        random.randint(0, (len(playlist.songs_list) - 1))]
                ws_manager2 = OBSWebsocketsManager()
                ws_manager2.play_audio(input_name, next_song)
                ws_manager2.current_playing_song = next_song
                ws_manager2.disconnect()

        random_song = playlist.songs_list[
            random.randint(0, (len(playlist.songs_list)-1))]
        self.play_audio(input_name, random_song)
        self.current_playing_song = random_song

        self.ws.eventmanager.register(play_next_song,
                                      events.MediaInputPlaybackEnded)

    def stop_playlist(self, input_name):  # stop the playlist playing in above func
        # stop all events listened to so no music will start
        self.ws.eventmanager.functions = []

        self.stop_audio(input_name)

    # Note this is a hacky way of doing this, but stopping the current song the eventmanager
    # will automatically pick a new song
    def skip_playlist(self, input_name):  # play a new song in this playlist
        self.stop_audio(input_name)

    def play_pause_audio(self, input_name):
        response = self.ws.call(requests.GetMediaInputStatus(inputName=input_name))
        media_state = response.datain['mediaState']
        if media_state == self.PLAYING:
            self.pause_audio(input_name)
        else:
            self.play_audio(input_name)

    def volume_up(self, input_name, amount=6):
        response = self.ws.call(requests.GetInputVolume(inputName=input_name))
        volume_db = response.datain['inputVolumeDb']
        volume_db += amount
        self.ws.call(requests.SetInputVolume(inputName=input_name, inputVolumeDb=volume_db))

    def volume_down(self, input_name, amount=6):
        response = self.ws.call(requests.GetInputVolume(inputName=input_name))
        volume_db = response.datain['inputVolumeDb']
        volume_db -= amount
        self.ws.call(requests.SetInputVolume(inputName=input_name, inputVolumeDb=volume_db))

    def toggle_input_mute(self, input_name):
        self.ws.call(requests.ToggleInputMute(inputName=input_name))
