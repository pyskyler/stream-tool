from . import _create_website
from ._website import Website


def create_website(use_obs_websockets=False) -> Website:
    """Create a web server with an index page

    Returns
    -------
    object: Website
        instance of class _website.Website

    Parameters
    ----------
    use_obs_websockets: Bool, default False
        If set to true the website creates an OBS websocket managaer to communicate with OBS Websockets

    Examples
    --------
    >>> from stream_tool import create_website
    >>> my_site = create_website()

    """
    created_website: Website = _create_website.create_website(use_obs_websockets)
    return created_website
