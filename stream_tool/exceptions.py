

class DuplicateError(Exception):
    pass


class DuplicateWebsiteError(DuplicateError):
    pass


class DuplicatePageNameError(DuplicateError):
    pass


class DuplicateButtonNameError(DuplicateError):
    pass


class ButtonNameSyntaxError(SyntaxError):
    pass
