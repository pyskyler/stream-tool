from __future__ import annotations

from flask import Flask, render_template

from typing import TYPE_CHECKING

from ._page import Page

from . import builtin_obs_actions

from ._create_obs_websocket_manager import create_obs_websocket_manager

if TYPE_CHECKING:
    from ._button import Button


class Website:
    """ A website and all its information

    Attributes
    ----------
    index_page
        The _page.Page object for the index page automatically created by the site
    ws
        An instance of obsws from package obs-websocket-py. Would be used to create custom OBS
        controls not provided in builtin_obs_actions and attach to a button function. Use its method
        call to perform custom actions. The OBS websockets manager created by the site if
        use_obs_websockets is True.

    """
    one_website_made: bool = False

    def __init__(self, use_obs_websockets=False):
        self._app = Flask(__name__, template_folder="resources/templates",
                          static_folder="resources/static", static_url_path="/static")
        self.all_pages: list[Page] = []
        self.all_page_names: dict[str, Page] = {}
        self.index_page = self.add_page('index')
        self.buttons_with_functions: dict[str, Button] = {}
        Website.one_website_made = True

        if use_obs_websockets:
            self.ws = create_obs_websocket_manager()
            builtin_obs_actions._ws = self.ws


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
        >>> import streamtool
        >>> my_site = create_website()
        >>> my_page = my_site.add_page('My-Page-Name')

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
        >>> import streamtool
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

        @self._app.route('/')
        def show_index():
            return render_template("page_template.html",
                                   part_2=self.all_page_names["index"].html_part_2,
                                   part_4=self.all_page_names["index"].html_part_4)

        @self._app.route('/<page_name>')
        def show_page(page_name):
            if page_name in self.all_page_names:
                return render_template("page_template.html",
                                       part_2=self.all_page_names[page_name].html_part_2,
                                       part_4=self.all_page_names[page_name].html_part_4)
            elif page_name in self.buttons_with_functions:
                this_button = self.buttons_with_functions[page_name]
                args = this_button.button_function_args
                kwargs = this_button.button_function_kwargs
                this_button.button_function(*args, **kwargs)
                return this_button.name
            else:
                return render_template("404.html"), 404

        self._app.run(host=host, port=port, debug=debug)
