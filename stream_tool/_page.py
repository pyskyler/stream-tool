from __future__ import annotations
from typing import TYPE_CHECKING

from ._button import Button
from .settings_objects import ButtonSettings

if TYPE_CHECKING:
    from ._website import Website
    from .settings_objects import PageSettings


class Page:
    """ A page and all its information

    Attributes
    ----------
    settings: PageSettings
            The settings object containing all the changeable settings for the page
    url: str
        This is a property that can get the relative url for this page on the website

    """
    def __init__(self, website: Website, settings: PageSettings):

        self.settings = settings

        self.website: Website = website
        self.all_buttons: list[Button] = []

        self.html_button_classes = ""
        self.button_colors_and_classes = {}
        self.html_part_2 = ""
        self.html_part_4 = ""

    # TODO: Make this work right
    @property
    def url(self):
        if self.settings.name != 'index':
            url = f"/{self.settings.name}"
        else:
            url = "/"
        return url

    def build(self):

        self.settings.check_required_settings()
        self.settings.check_for_duplicate_name()

        button_colors = []

        for button in self.all_buttons:
            new_color = (button.settings.color != "default") and (button.settings.color not in button_colors)
            if new_color:
                button_colors.append(button.settings.color)

        for i in range(len(button_colors)):
            if i == 0:
                self.html_button_classes += f"\t\t"
            this_color = button_colors[i]
            this_color_class = f".button{i} {{background-color: {this_color};}} \n\t\t"

            self.html_button_classes += this_color_class

            self.button_colors_and_classes[this_color] = f"button{i}"

        for button in self.all_buttons:
            button.build()

    def add_button(self, settings: ButtonSettings = None) -> Button:
        """ Add a button to a page

        Parameters
        ----------
        settings: ButtonSettings, optional
            The settings object containing all the changeable settings for the button, if not passed
             in, one will be created automatically.

        Returns
        -------
        object: Button
            instance of Button class

        Examples
        --------
        >>> import streamtool
        >>> my_site = create_website()
        >>> my_page = my_site.add_page()
        >>> my_button = my_page.add_button()

        """
        if settings is None:
            settings = ButtonSettings()

        added_button: Button = Button(self, settings)
        self.all_buttons.append(added_button)
        return added_button
