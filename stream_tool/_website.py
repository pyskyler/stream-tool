from __future__ import annotations

from flask import Flask, render_template

from typing import TYPE_CHECKING

from ._page import Page

from . import builtin_obs_actions

from ._create_obs_websocket_manager import create_obs_websocket_manager

from ._generators import ButtonNameGenerator

from .settings_objects import PageSettings

if TYPE_CHECKING:
    from ._button import Button
    from .settings_objects import WebsiteSettings


class Website:
    """ A website and all its information

    Attributes
    ----------
    settings: PageSettings
        The settings object containing all the changeable settings for the page
    index_page page
        The _page.Page object for the index page automatically created by the site
    ws
        An instance of obsws from package obs-websocket-py. Would be used to create custom OBS
        controls not provided in builtin_obs_actions and attach to a button function. Use its method
        call to perform custom actions. The OBS websockets manager created by the site if
        use_obs_websockets is True.
    app
        The Flask app object


    """
    one_website_made: bool = False

    def __init__(self, settings: WebsiteSettings):
        self.settings = settings

        self.app = Flask(__name__, template_folder="resources/templates",
                         static_folder="resources/static", static_url_path="/static")
        self.all_pages: list[Page] = []
        self.pages_and_names: dict[str, Page] = {}

        index_page_settings = PageSettings()
        index_page_settings.name = "index"
        self.index_page = self.add_page(index_page_settings)

        Website.one_website_made = True

        self.button_name_generator = ButtonNameGenerator()

        if settings.use_obs_websockets:
            self.ws = create_obs_websocket_manager(settings)
            builtin_obs_actions._ws = self.ws

    def add_page(self, settings: PageSettings = None) -> Page:
        """ Add a page on the website

        Parameters
        ----------
        settings: PageSettings, optional
            The settings object containing all the changeable settings for the page, if not passed
             in, one will be created automatically.

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
        if settings is None:
            settings = PageSettings()

        created_page: Page = Page(self, settings)
        self.all_pages.append(created_page)
        return created_page

    def _build(self):
        self.settings.check_required_settings()

        self.buttons_with_functions: dict[str, Button] = {}
        for page in self.all_pages:
            for button in page.all_buttons:
                if button.settings.function is not None:
                    self.buttons_with_functions[button.name] = button

        self.pages_and_names: dict[str, Page] = {page.settings.name: page for page in self.all_pages}

        for page in self.all_pages:
            page.build()

        @self.app.route('/')
        def show_index():
            return render_template("page_template.html",
                                   button_color=self.pages_and_names["index"].settings.button_color,
                                   colors=self.pages_and_names["index"].html_button_classes,
                                   part_2=self.pages_and_names["index"].html_part_2,
                                   part_4=self.pages_and_names["index"].html_part_4)

        @self.app.route('/<page_name>')
        def show_page(page_name):
            if page_name in self.pages_and_names:
                return render_template("page_template.html",
                                       button_color=self.pages_and_names[page_name].settings.button_color,
                                       colors=self.pages_and_names[page_name].html_button_classes,
                                       part_2=self.pages_and_names[page_name].html_part_2,
                                       part_4=self.pages_and_names[page_name].html_part_4)
            elif page_name in self.buttons_with_functions:
                this_button = self.buttons_with_functions[page_name]
                args = this_button.settings.function_args
                kwargs = this_button.settings.function_kwargs
                this_button.settings.function(*args, **kwargs)
                return this_button.name
            else:
                return render_template("404.html"), 404

    def _run(self, host='127.0.0.1', port=5000, debug=False):

        self.app.run(host=host, port=port, debug=debug)

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

        self._build()

        self._run(host, port, debug)
