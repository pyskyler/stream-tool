from __future__ import annotations

import os

from .exceptions import DuplicatePageNameError
from ._data import restricted_use_names

from typing import TYPE_CHECKING

from ._button import Button
if TYPE_CHECKING:
    from ._website import Website


class Page:
    """ A page and all its information

    Attributes
    ----------
    name: str
        name of page displayed in tab
    url: str
        this is a property that can get the relative url for this page on the website

    """
    def __init__(self, website: Website, name):
        self._name: str | None = None
        self.website: Website = website
        self.name = name
        self.all_buttons: list[Button] = []
        self.all_button_names: list[str] = []

        self.html_part1_path = f"html_creation_files/standard_files/html_file_part1.txt"
        self.html_part3_path = f"html_creation_files/standard_files/html_file_part3.txt"
        self.html_part5_path = f"html_creation_files/standard_files/html_file_part5.txt"

    @property
    def html_part2_path(self):
        return f"html_creation_files/{self.name}/html_file_part2.txt"

    @property
    def html_part4_path(self):
        return f"html_creation_files/{self.name}/html_file_part4.txt"

    @property
    def _html_directory_path(self):
        return f"html_creation_files/{self.name}"

    @property
    def _html_template_path(self):
        return f"templates/{self.name}.html"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self.name is not None:
            previous_name = self.name
            previous_html_directory_path = f"html_creation_files/{previous_name}"

            restricted_use_names.remove(previous_name)

            self.website.all_page_names.remove(previous_name)

            os.rmdir(previous_html_directory_path)

        self._name = name

        if name in restricted_use_names:
            if name in self.website.all_page_names:
                raise DuplicatePageNameError(f"Page name {name} already in use. Use a different name.")
            else:
                raise DuplicatePageNameError(f"Page name {name} is not allowed to be used. Use a different name. "
                                             f"Restricted use names are in list main.restricted_use_names. "
                                             f"They are currently: {restricted_use_names}")

        restricted_use_names.append(name)

        self.website.all_page_names.append(name)

        os.mkdir(self._html_directory_path)

    @property
    def url(self):
        url = f"/{self.name}"
        return url

    def add_button(self, name: str, **kwargs) -> Button:
        """ Add a button to a page

        Parameters
        ----------
        name: str
            The name of the button
        **kwargs: dict, optional
            Extra arguments for creating button, refer to Button class for keyword arguments

        Returns
        -------
        object: Button
            instance of class _button.Button

        Examples
        --------
        >>> from main import create_website
        >>> my_site = create_website()
        >>> my_page = my_site.add_page()
        >>> my_button = my_page.add_button("button name")

        """
        added_button: Button = Button(self, name, **kwargs)
        self.all_buttons.append(added_button)
        return added_button

    def build(self):
        """ Build the page files

        Takes each part of the html file that has been constructed and puts them together

        """
        with open(self.html_part1_path, "r") as part1:
            part1 = part1.read()
        if os.path.isfile(self.html_part2_path):
            with open(self.html_part2_path, "r") as part2:
                part2 = part2.read()
        else:
            part2 = "\n"
        with open(self.html_part3_path, "r") as part3:
            part3 = part3.read()
        if os.path.isfile(self.html_part4_path):
            with open(self.html_part4_path, "r") as part4:
                part4 = part4.read()
        else:
            part4 = "\n"
        with open(self.html_part5_path, "r") as part5:
            part5 = part5.read()

        full_file = part1 + part2 + part3 + part4 + part5

        with open(self._html_template_path, "w") as file:
            file.write(full_file)

    def delete_build_files(self):
        """ Delete the files used to make page html

        """
        if os.path.isfile(self.html_part2_path):
            os.remove(self.html_part2_path)
        if os.path.isfile(self.html_part4_path):
            os.remove(self.html_part4_path)
        if os.path.isdir(self._html_directory_path):
            os.rmdir(self._html_directory_path)
