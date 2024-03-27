from .exceptions import InvalidSettingName, DuplicateNameError, MissingRequiredSettingError
from ._formatting_and_converting import format_page_name, format_and_check_color, format_url


class BaseSettings:

    restricted_use_names = set()

    def __init__(self):
        self._object_type = None
        self._required_settings = None
        self._excluded_attrs = ['_object_type', '_required_settings', '_excluded_attrs']

    @property
    def object_type(self):
        return self._object_type

    def set(self, settings: dict):
        for key, value in settings.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise InvalidSettingName(key, self.object_type)
    pass

    def get(self):
        # dict comprehension to pull all the attributes of self except the ones in self._excluded_attrs
        output = {key: value for key, value in self.__dict__.items() if key not in self._excluded_attrs}
        return output

    def check_if_name_restricted_and_add(self, name):
        if name in self.restricted_use_names:
            raise DuplicateNameError(name, self.restricted_use_names)
        self.restricted_use_names.add(name)

    def replace_restricted_name(self, old_name, new_name):
        self.restricted_use_names.remove(old_name)
        self.check_if_name_restricted_and_add(new_name)

    def reset_restricted_names(self):
        self.restricted_use_names = set()

    def check_required_settings(self):
        if self._required_settings is None:
            return
        for setting in self._required_settings:
            if getattr(self, setting) is None:
                raise MissingRequiredSettingError(setting, self.object_type)


class WebsiteSettings(BaseSettings):

    """
    use_obs_websockets: Bool, default False
        If set to true the website creates an OBS websocket managaer to communicate with OBS Websockets
    websocket_host: str
        The ip address of the websockets server to communicate with. Set to '127.0.0.1' by default
        which is the local machine address.
    websocket_port: int
        The port to connect to on the websockets server. Set to 4455 by default which is the OBS default.
    websocket_password: str
        The password to connect to the OBS websockets server. Empty by default
    """

    def __init__(self):
        super().__init__()
        self._object_type = "Website"
        self.use_obs_websockets = False  # default value
        self.websocket_host = "127.0.0.1"
        self.websocket_port = 4455
        self.websocket_password = ""


class PageSettings(BaseSettings):
    """
    name: str
        The url for the page. Spaces will be replaced with dashes.
    url: str
        This is a property that can get the relative url for this page on the website
    button_color: str
        the default color for the buttons on the page, default is "#3498db".
        follows the same rules as the color attribute of Button class
        """
    def __init__(self):
        super().__init__()
        self._required_settings = ["name"]
        self._object_type = "Page"

        self._name: str = None
        self.name: str = None  # required value

        self._button_color: str = None
        self.button_color: str = '3498DB'  # default value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name is not None:
            name = format_page_name(name)
        self._name = name

    @property
    def button_color(self):
        return self._button_color

    @button_color.setter
    def button_color(self, button_color):
        self._button_color = format_and_check_color(button_color)

    def check_for_duplicate_name(self):
        self.check_if_name_restricted_and_add(self.name)


class ButtonSettings(BaseSettings):

    """

        Attributes
        ----------
        name: str
            The name of the button
        text: str
            Text for the button, defaults to the name parameter
        color: str
            Color of the button, defaults to "defualt" which is blue. Set it to a valid css color
            name or a valid rgb hex color.
        button_function: callable
            Action for button to run on press
        button_function_args: list, Any
            Arguments or single argument to be passed to button_function
        button_function_kwargs: dict,
            Keyword arguments to be passed to button_function
        button_link: str
            A url to a relative page on the site or any page on the web
    """

    def __init__(self):
        super().__init__()
        self._object_type = "Button"

        self.text: str = "Test Text"  # default value
        self.function = None  # default value
        self.function_args: list = []  # default value
        self.function_kwargs: dict = {}  # default value
        self._color: str = 'default'
        self.color: str = 'default'  # default value
        self._link = None
        self.link = None  # default value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, link):
        if link is None:
            self._link = link
        else:
            self._link = format_url(link)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if color == "default":
            self._color = color
            return
        self._color = format_and_check_color(color)
