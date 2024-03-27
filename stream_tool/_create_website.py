from .exceptions import *

from ._website import Website
from .settings_objects import WebsiteSettings


def create_website(settings) -> Website:
    if settings is None:
        settings = WebsiteSettings()
    if Website.one_website_made:
        raise DuplicateWebsiteError("Another website is being created. Only one website can exist and already does.")

    website: Website = Website(settings)
    return website
