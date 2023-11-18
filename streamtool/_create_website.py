from .exceptions import *

from ._website import Website


def create_website(*args) -> Website:
    if Website.one_website_made:
        raise DuplicateWebsiteError("Another website is being created. Only one website can exist and already does.")

    website: Website = Website(*args)
    return website
