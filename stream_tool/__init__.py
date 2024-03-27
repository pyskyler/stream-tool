"""
stream-tool

A package for programmatically creating a web server with page and buttons for controlling tools needed for
streaming to platforms and using OBS websockets to communicate with OBS.

Modules
-------
Websockets_Auth
    The information needed to connect to websockets: host, port, password.
builtin_obs_actions
    Actions to perform on OBS websockets


Classes
-------
WebsiteSettings
    Settings object for changing settings and preferences of the website.
PageSettings
    Settings object for changing settings and preferences of the pages.
ButtonSettings
    Settings object for changing settings and preferences of the buttons.

Functions
---------
create_website
    Creates a website object and returns it. This object is where everything is created from.

Error Handling
--------------
These are the custom errors that can be raised by the program:

-- DuplicateError

-- DuplicateWebsiteError

-- InvalidColorValueError

-- InvalidSettingName

-- DuplicateNameError

-- MissingRequiredSettingsError

The exceptions docstring contains more about their meaning

"""

from ._core import create_website, WebsiteSettings, PageSettings, ButtonSettings
from .exceptions import *
from .builtin_obs_actions import *

__all__ = ["create_website",
           "WebsiteSettings",
           "PageSettings",
           "ButtonSettings",
           "DuplicateError",
           "DuplicateWebsiteError",
           "InvalidColorValueError",
           "InvalidSettingName",
           "DuplicateNameError",
           "MissingRequiredSettingError",
           "builtin_obs_actions"]
