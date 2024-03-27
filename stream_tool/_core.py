from . import _create_website
from ._website import Website
from .settings_objects import WebsiteSettings, PageSettings, ButtonSettings


def create_website(settings: WebsiteSettings = None) -> Website:
    """Create a web server with an index page

    Returns
    -------
    object: Website
        instance of class _website.Website

    Parameters
    ----------
    settings: WebsiteSettings, optional
        The settings object containing all the changeable settings for the website, if not passed
         in, one will be created automatically.


    Examples
    --------
    >>> from stream_tool import create_website
    >>> my_site = create_website()

    """

    created_website: Website = _create_website.create_website(settings)
    return created_website


WebsiteSettings = WebsiteSettings
PageSettings = PageSettings
ButtonSettings = ButtonSettings
