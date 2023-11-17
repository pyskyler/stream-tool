from __future__ import annotations

import os

from flask import Flask, render_template

from typing import TYPE_CHECKING

from _page import Page

import _data

from _create_obs_websocket_manager import create_obs_websocket_manager

if TYPE_CHECKING:
    from _button import Button


class Website:
    """ A website and all its information

    Attributes
    ----------
    index_page
        The _page.Page object for the index page automatically created by the site
    ws
        The OBS websockets manager created by the site if use_obs_websockets is true. Would be used to create custom
        OBS controls not provided in builtin_obs_actions and attach to a button function.
    """
    one_website_made: bool = False

    def __init__(self, use_obs_websockets=False):
        self._app = Flask(__name__)
        self.all_pages: list[Page] = []
        self.all_page_names: list = []
        self.index_page = self.add_page('index')
        self.buttons_with_functions: dict[str, Button] = {}
        Website.one_website_made = True

        reset_server_files()

        # setup use of images for 404 page
        self._app.static_folder = 'static'
        self._app.static_url_path = '/static'

        if use_obs_websockets:
            self.ws = create_obs_websocket_manager()
            _data.obs_websocket_manager = self.ws

    def add_page(self, name: str) -> Page:
        """ Add a page on the website

        Parameters
        ----------
        name : str
            name of page displayed in tab

        Returns
        -------
        object: Page
            instance of class _page.Page

        Examples
        --------
        >>> from StreamTool import create_website
        >>> my_site = create_website()
        >>> my_page = my_site.add_page('My Page Name')

        """
        created_page: Page = Page(self, name)
        self.all_pages.append(created_page)
        return created_page

    def build_and_run(self, host="127.0.0.1", port=5000, debug=False):
        """ Build website files and routes and run it

        This function of the Website class builds the whole website including
        each page and all its buttons. It creates every html file. It also
        gives Flask a function to send that html to each user. It also runs
        the website on the web server.



        Examples
        --------
        >>> from main import create_website
        >>> my_site = create_website()
        >>> my_site.build_and_run()

        Parameters
        ----------
        host: str {'127.0.0.1', '0.0.0.0'}
            The host to run the web server on. Defaults to '127.0.0.1' which runs the
            server locally. Set this to '0.0.0.0' to have the server available
            externally as well.
        port: int, default 5000
            The port to run the web server on.
        debug: bool, default False
            Run flask in debug. Default is off.


        """
        for page in self.all_pages:
            for button in page.all_buttons:
                button.build()
            page.build()
            page.delete_build_files()

        @self._app.route('/')
        def show_index():
            return render_template('index.html')

        @self._app.route('/<page_name>')
        def show_page(page_name):
            if page_name in self.all_page_names:
                return render_template(f"{page_name}.html")
            elif page_name in self.buttons_with_functions:
                this_button = self.buttons_with_functions[page_name]
                this_button.button_function()
                return this_button.name
            else:
                return render_template("404.html")

        self._app.run(host=host, port=port, debug=debug)


def reset_server_files():
    for file in os.listdir("templates"):
        if file != "404.html":
            os.remove(f"templates/{file}")
    for directory in os.listdir("html_creation_files"):
        if directory != "standard_files" and os.path.isdir(f"html_creation_files/{directory}"):
            for file in os.listdir(f"html_creation_files/{directory}"):
                os.remove(f"html_creation_files/{directory}/{file}")
            os.rmdir(f"html_creation_files/{directory}")
