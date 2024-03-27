"""All the custom exceptions that can be raised"""


class DuplicateError(Exception):
    """More than one of something in the website"""
    pass


class DuplicateWebsiteError(DuplicateError):
    """More than one website created"""
    pass


class InvalidColorValueError(ValueError):
    """Not a valid CSS color name or not valid css color hex number"""
    pass


class InvalidSettingName(Exception):
    """The setting that is trying to be changed does not exist for this object"""
    def __init__(self, setting_name, object_type):
        self.setting_name = setting_name
        self.objectType = object_type
        self.message = f"Invalid setting: {setting_name}, for object: {object_type}"
        super().__init__(self.message)


class DuplicateNameError(DuplicateError):
    """More than one object of the same name in the website that is not allowed to share a name."""

    def __init__(self, name, restricted_names):
        self.name = name
        self.restricted_names = restricted_names
        self.message = f"Duplicate name {name} cannot be used. These names have been used cannot be used:" \
                       f" {restricted_names}"
        super().__init__(self.message)


class MissingRequiredSettingError(Exception):
    """When trying to build the website a required setting is missing"""
    def __init__(self, setting_name, object_type):
        self.message = f"Required setting '{setting_name}' is missing for object type '{object_type}'."
        super().__init__(self.message)
