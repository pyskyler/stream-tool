""" Actions to perform on OBS websockets

Has a set of functions that can be run to tell OBS to do something. These can be attached to buttons
to make them happen on a button click.

"""
from . import _data
from obswebsocket import requests

# TODO: share (obs websocket?) errors with user
# TODO: create error handlign for trying to use obs functions wihtout use_obs_websockets enabled
#  could be on button press or could be done in the build and run step in some way

_PLAY_INPUT = "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY"
_STOP_INPUT = "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_STOP"
_PAUSE_INPUT = "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE"

_PLAYING = "OBS_MEDIA_STATE_PLAYING"
_PAUSED = "OBS_MEDIA_STATE_PAUSED"

_ws = None


def disconnect():
    """Disconnect the web socket connection

    """
    _ws.disconnect()


def set_scene(new_scene):
    """Set the current scene (or program scene if using studio mode)

    Parameters
    ----------
    new_scene: str
        The name of the scene to set to

    """
    _ws.call(requests.SetCurrentProgramScene(sceneName=new_scene))


def set_filter_visibility(source_name, filter_name, filter_enabled=True):
    """Set a source filter visibility

    Parameters
    ----------
    source_name: str
        The name of the source to affect
    filter_name: str
        The name of the filter to affect
    filter_enabled: bool, optional True
        Set the filter enable (visible) status, default is True (enabled or visible)

    """
    _ws.call(requests.SetSourceFilterEnabled(
        sourceName=source_name, filterName=filter_name, filterEnabled=filter_enabled))


def set_source_visibility(scene_name, source_name, source_visible=True):
    """Set a source visibility

    Parameters
    ----------
    scene_name: str
        The name of the scene containing the source to affect
    source_name: str
        The name of the source to affect
    source_visible: bool, optional True
        Set to source enable (visible) status, default is True (enabled or visible)

    """
    response = _ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
    my_item_id = response.datain['sceneItemId']
    _ws.call(requests.SetSceneItemEnabled(sceneName=scene_name, sceneItemId=my_item_id, sceneItemEnabled=source_visible))


def get_text(source_name):
    """ Get the current text of a text source

    Parameters
    ----------
    source_name
        the text source to get the current text of

    Returns
    -------
    text: str
        the current text of the source

    """
    response = _ws.call(requests.GetInputSettings(inputName=source_name))
    return response.datain["inputSettings"]["text"]


# Returns the text of a text source
def set_text(source_name, new_text):
    """ Set the text of a text source

    Parameters
    ----------
    source_name: str
        The name of text source to change
    new_text: srt
        The text to set the source to

    """
    _ws.call(requests.SetInputSettings(inputName=source_name, inputSettings={'text': new_text}))


def get_source_transform(scene_name, source_name):
    """ The current transform effects on a source

    Used in combination with set_source_transform to change the transform values of a source.
    Keys in the return dictionary are: positionX, positionY, scaleX, scaleY, cropTop, cropBottom,
    cropLeft, cropRight, rotation. See: set_source_transform.

    Parameters
    ----------
    scene_name: str
        The name of the scene containing the source to get transform
    source_name: str
        The name of the source to get transform

    Returns
    -------
    dict
        Every aspect that can be transformed as a key and its current value as the value

    Examples
    --------
    >>> import stream_tool
    >>> source_current_transform =
    ...     builtin_obs_actions.get_source_transform(
    ...         "my scene 1", "source I want to change")
    >>> source_new_transform = source_current_transform
    >>> # Move 100 pixels to the right
    >>> source_new_transform["positionX"] += 100
    >>> # set bottom crop to 50
    >>> source_new_transform["cropBottom"] = 50
    >>> builtin_obs_actions.set_source_transform(
    ...     "my scene 1",
    ...     "source I want to change",
    ...     source_new_transform)

    """
    response = _ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
    my_item_id = response.datain['sceneItemId']
    response = _ws.call(requests.GetSceneItemTransform(sceneName=scene_name, sceneItemId=my_item_id))
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


def set_source_transform(scene_name, source_name, new_transform):
    """ Set the transform values for a source

    The transform should be a dictionary containing any of the following keys with corresponding values
    positionX, positionY, scaleX, scaleY, cropTop, cropBottom, cropLeft, cropRight, rotation. The
    current status can be retrieved with get_source_transform.

    Parameters
    ----------
    scene_name: str
        the name of the scene containing the source to affect
    source_name: str
        the name of the source to affect
    new_transform: dict
        dictionary containing keys of property to change and the value to set it to. Can get the current values
        with get_source_transform or just set the desired keys

    Examples
    --------
    >>> import stream_tool
    >>> transform = {"scaleX": 2,
    ...              "scaleY": 3}
    >>> set_source_transform("my scene 1", "source I want to change", transform)

    This is an alternate example using get_source_transform to update relative to current values

    >>> import stream_tool
    >>> source_current_transform = builtin_obs_actions.get_source_transform("my scene 1", "source I want to change")
    >>> source_new_transform = source_current_transform
    >>> # Move 100 pixels to the right
    >>> source_new_transform["positionX"] += 100
    >>> builtin_obs_actions.set_source_transform("my scene 1", "source I want to change", source_new_transform)


    """
    response = _ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
    my_item_id = response.datain['sceneItemId']
    _ws.call(requests.SetSceneItemTransform(
        sceneName=scene_name, sceneItemId=my_item_id, sceneItemTransform=new_transform))


def get_input_settings(input_name):
    """ Get the settings for an input

    To be used with set_input_settings which requires the object this returns

    Parameters
    ----------
    input_name: str
        name of the input to get settings for

    Returns
    -------
    object
        all the settings of the input

    Notes
    -----
    an input, like a text box, is a type of source. This will get *input-specific settings*, not the broader
    source settings like transform and scale
    For a text source, this will return settings like its font, color, etc

    """
    return _ws.call(requests.GetInputSettings(inputName=input_name))


def set_input_settings(input_name, input_settings):
    """ Set the settings of an input with a version of the object retrieved from get_input_settings

    Parameters
    ----------
    input_name: str
        the name of the input to set settings
    input_settings: object
        returned from get_input_settings and can then be edited

    """
    _ws.call(requests.SetInputSettings(inputName=input_name, inputSettings=input_settings))


# TODO: check what this actually does
def get_scene_items(scene_name):
    """ Get all names of items in a scene

    Parameters
    ----------
    scene_name: str
        name of the scene to get items from

    Returns
    -------
    list
        names of items in the scene

    """
    return _ws.call(requests.GetSceneItemList(sceneName=scene_name))


def transition_to_scene(scene_name, transition_name):
    """Transition to a scene in studio mode

    This puts a scene in preview and then runs a transition to go to that scene.

    Parameters
    ----------
    scene_name: str
        The name of the scene to transition to
    transition_name: str
        The name of the transition to use

    """
    _ws.call(requests.SetCurrentPreviewScene(sceneName=scene_name))
    _ws.call(requests.SetCurrentSceneTransition(transitionName=transition_name))
    _ws.call(requests.TriggerStudioModeTransition())


def get_current_program_scene():
    """ Get the current live scene (or program scene if in studio mode)

    Returns
    -------
    current_scene: str
        The name of the current scene (or current program scene if in studio mode)

    """
    response = _ws.call(requests.GetCurrentProgramScene())
    current_scene = response.datain['currentProgramSceneName']
    return current_scene


def pause_audio(input_name):
    """ Pause audio playback on an audio input

        Parameters
        ----------
        input_name: str
            The audio input to affect

        """
    _ws.call(requests.TriggerMediaInputAction(inputName=input_name, mediaAction=_PAUSE_INPUT))


def stop_audio(input_name):
    """ Stop audio playback on an audio input

    Parameters
    ----------
    input_name: str
        The audio input to affect

    """
    _ws.call(requests.TriggerMediaInputAction(inputName=input_name, mediaAction=_STOP_INPUT))


# File to play is optional
def play_audio(input_name, file_path=None):
    """Play audio from a file, if no file is provided it will just play the input

    Parameters
    ----------
    input_name: str
        The audio input to affect
    file_path: str, optional
        The file path of the audio file to play on the system with OBS

    Returns
    -------

    """
    if file_path is not None:
        response = get_input_settings(input_name)

        input_settings = response.datain['inputSettings']  # Change file Name to be the value passed into func
        input_settings['local_file'] = file_path
        set_input_settings(input_name, input_settings)

    _ws.call(requests.TriggerMediaInputAction(inputName=input_name, mediaAction=_PLAY_INPUT))


def play_pause_audio(input_name):
    """Toggle play/pause on an audio input

    Parameters
    ----------
    input_name: str
        name of the input to affect

    """
    response = _ws.call(requests.GetMediaInputStatus(inputName=input_name))
    media_state = response.datain['mediaState']
    if media_state == _PLAYING:
        pause_audio(input_name)
    else:
        play_audio(input_name)


def change_volume(input_name, amount=6):
    """ Change volume by a dB amount, default is 6 dB,

    Use negative dB amount to turn down and a positive dB to turn up

    Parameters
    ----------
    input_name: str
        the name of the input to affect
    amount: int, optional 6
        number of dB to change by, default is 6 dB

    """
    response = _ws.call(requests.GetInputVolume(inputName=input_name))
    volume_db = response.datain['inputVolumeDb']
    volume_db += amount
    _ws.call(requests.SetInputVolume(inputName=input_name, inputVolumeDb=volume_db))


def toggle_input_mute(input_name):
    """ Toggle the mute status of an input

    Parameters
    ----------
    input_name: str
        the input to affect

    """
    _ws.call(requests.ToggleInputMute(inputName=input_name))
