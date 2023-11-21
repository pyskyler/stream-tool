from __future__ import annotations

from .exceptions import DuplicatePageNameError
from ._data import restricted_use_names
from._formatting_and_converting import format_page_name

from typing import TYPE_CHECKING

from ._button import Button
if TYPE_CHECKING:
    from ._website import Website


class Page:
    """ A page and all its information

    Attributes
    ----------
    name: str
        The url for the page. Spaces will be replaced with dashes.
    url: str
        This is a property that can get the relative url for this page on the website

    """
    def __init__(self, website: Website, name):
        self._name: str | None = None
        self.website: Website = website
        self.name = name
        self.all_buttons: list[Button] = []
        self.all_button_names: list[str] = []

        self.html_part_2 = ""
        self.html_part_4 = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self.name is not None:
            previous_name = self.name

            restricted_use_names.remove(previous_name)

            self.website.all_page_names.pop(previous_name)

        name = format_page_name(name)

        self._name = name

        if name in restricted_use_names:
            if name in self.website.all_page_names:
                raise DuplicatePageNameError(f"Page name {name} already in use. Use a different name.")
            else:
                raise DuplicatePageNameError(f"Page name {name} is not allowed to be used. Use a different name. "
                                             f"Restricted use names are in list main.restricted_use_names. "
                                             f"They are currently: {restricted_use_names}")

        restricted_use_names.append(name)

        self.website.all_page_names[name] = self

    # TODO: Make this work right
    @property
    def url(self):
        if self.name != 'index':
            url = f"/{self.name}"
        else:
            url = "/"
        return url

    def add_button(self, name: str, **kwargs) -> Button:
        """ Add a button to a page

        Parameters
        ----------
        name: str
            The name of the button
        **kwargs: dict, optional
            Extra arguments for creating button, refer to Button class docmentation for keyword arguments

        Returns
        -------
        object: Button
            instance of Button class

        Examples
        --------
        >>> import streamtool
        >>> my_site = create_website()
        >>> my_page = my_site.add_page()
        >>> my_button = my_page.add_button("button name")

        """
        added_button: Button = Button(self, name, **kwargs)
        self.all_buttons.append(added_button)
        return added_button
