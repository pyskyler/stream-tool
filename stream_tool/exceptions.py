"""All the custom exceptions that can be raised"""


class DuplicateError(Exception):
    """More than one of something in the website"""
    pass


class DuplicateWebsiteError(DuplicateError):
    """More than one website created"""
    pass


class DuplicatePageNameError(DuplicateError):
    """More than one of the same page name created"""
    pass


class DuplicateButtonNameError(DuplicateError):
    """More than one of the same button name created"""
    pass


class ButtonNameSyntaxError(SyntaxError):
    """Button name includes invalid syntax for a button name"""
    pass
