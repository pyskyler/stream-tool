from . import _data
from obswebsocket import requests

_PLAY_INPUT = "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY"
_STOP_INPUT = "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_STOP"
_PAUSE_INPUT = "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE"

_PLAYING = "OBS_MEDIA_STATE_PLAYING"
_PAUSED = "OBS_MEDIA_STATE_PAUSED"

ws = _data.obs_websocket_manager


def disconnect():
    ws.disconnect()


# Set the current scene
def set_scene(new_scene):
    ws.call(requests.SetCurrentProgramScene(sceneName=new_scene))


# Set the visibility of any source's filters
def set_filter_visibility(source_name, filter_name, filter_enabled=True):
    ws.call(requests.SetSourceFilterEnabled(
        sourceName=source_name, filterName=filter_name, filterEnabled=filter_enabled))


# Set the visibility of any source
def set_source_visibility(scene_name, source_name, source_visible=True):
    response = ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
    my_item_id = response.datain['sceneItemId']
    ws.call(requests.SetSceneItemEnabled(sceneName=scene_name, sceneItemId=my_item_id, sceneItemEnabled=source_visible))


# Returns the current text of a text source
def get_text(source_name):
    response = ws.call(requests.GetInputSettings(inputName=source_name))
    return response.datain["inputSettings"]["text"]


# Returns the text of a text source
def set_text(source_name, new_text):
    ws.call(requests.SetInputSettings(inputName=source_name, inputSettings={'text': new_text}))


def get_source_transform(scene_name, source_name):
    response = ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
    my_item_id = response.datain['sceneItemId']
    response = ws.call(requests.GetSceneItemTransform(sceneName=scene_name, sceneItemId=my_item_id))
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
# Note: there are other transform settings, like height, width, sourceHeight, sourceWidth, alignment, etc., but these
# feel like the main useful ones.
# Use get_source_transform to see the full list
def set_source_transform(scene_name, source_name, new_transform):
    response = ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
    my_item_id = response.datain['sceneItemId']
    ws.call(requests.SetSceneItemTransform(
        sceneName=scene_name, sceneItemId=my_item_id, sceneItemTransform=new_transform))


# Note: an input, like a text box, is a type of source. This will get *input-specific settings*, not the broader
# source settings like transform and scale
# For a text source, this will return settings like its font, color, etc
def get_input_settings(input_name):
    return ws.call(requests.GetInputSettings(inputName=input_name))


# set the input settings, input settings takes an object that can be retrieved from the above function
def set_input_settings(input_name, input_settings):
    ws.call(requests.SetInputSettings(inputName=input_name, inputSettings=input_settings))


# Get list of all the input types
def get_input_kind_list():
    return ws.call(requests.GetInputKindList())


# Get list of all items in a certain scene
def get_scene_items(scene_name):
    return ws.call(requests.GetSceneItemList(sceneName=scene_name))


def transition_to_scene(scene_name, transition_name):
    ws.call(requests.SetCurrentPreviewScene(sceneName=scene_name))
    ws.call(requests.SetCurrentSceneTransition(transitionName=transition_name))
    ws.call(requests.TriggerStudioModeTransition())


def get_current_program_scene():
    response = ws.call(requests.GetCurrentProgramScene())
    current_scene = response.datain['currentProgramSceneName']
    return current_scene


def pause_audio(input_name):
    ws.call(requests.TriggerMediaInputAction(inputName=input_name, mediaAction=_PAUSE_INPUT))


def stop_audio(input_name):
    ws.call(requests.TriggerMediaInputAction(inputName=input_name, mediaAction=_STOP_INPUT))


# File to play is optional
def play_audio(input_name, file_path=None):
    if file_path is not None:
        response = get_input_settings(input_name)

        input_settings = response.datain['inputSettings']  # Change file Name to be the value passed into func
        input_settings['local_file'] = file_path
        set_input_settings(input_name, input_settings)

    ws.call(requests.TriggerMediaInputAction(inputName=input_name, mediaAction=_PLAY_INPUT))


def play_pause_audio(input_name):
    response = ws.call(requests.GetMediaInputStatus(inputName=input_name))
    media_state = response.datain['mediaState']
    if media_state == _PLAYING:
        pause_audio(input_name)
    else:
        play_audio(input_name)


def volume_up(input_name, amount=6):
    response = ws.call(requests.GetInputVolume(inputName=input_name))
    volume_db = response.datain['inputVolumeDb']
    volume_db += amount
    ws.call(requests.SetInputVolume(inputName=input_name, inputVolumeDb=volume_db))


def volume_down(input_name, amount=6):
    response = ws.call(requests.GetInputVolume(inputName=input_name))
    volume_db = response.datain['inputVolumeDb']
    volume_db -= amount
    ws.call(requests.SetInputVolume(inputName=input_name, inputVolumeDb=volume_db))


def toggle_input_mute(input_name):
    ws.call(requests.ToggleInputMute(inputName=input_name))
