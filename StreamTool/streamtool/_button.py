from __future__ import annotations

from _formatting_and_converting import convert_to_pascal_case, format_url
from .exceptions import DuplicateButtonNameError, ButtonNameSyntaxError
from ._data import restricted_use_names

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ._page import Page


class Button:
    """ A button and all its information

        Parameters
        ----------
        name: str
            The name of the button
        button_function: callable, optional
            Action for button to run on press
        text: str, optional
            text for the button, defaults to the name parameter
        button_link: str, optional
            a url to a relative page on the site or any page on the web


        Attributes
        ----------
        text: str
            The text label that appears on the button

        """

    def __init__(self, page: "Page", name: str, button_function: callable = None, text: str = None,
                 button_link: str = None):
        # TODO: make it so that people can specify parameters out of order by name
        self._button_function = None
        self.page: "Page" = page
        self._name = None
        self.name: str = name
        if text is None:
            self.text = self.name
        else:
            self.text = text
        self.button_function = button_function
        self.button_link = button_link

    @property
    def button_function(self):
        return self._button_function

    @button_function.setter
    def button_function(self, function):
        self._button_function = function
        if self.button_function is not None:
            self.page.website.buttons_with_functions[self.name]: Button = self

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        previous_name = self.name
        name = convert_to_pascal_case(name)
        self._name = name

        if name in restricted_use_names:
            if name in self.page.all_button_names:
                raise DuplicateButtonNameError(f"Button name {name} already in use. Use a different name.")
            else:
                raise DuplicateButtonNameError(f"Button name {name} is not allowed to be used. Use a different name. "
                                               f"Restricted use names are in list main.restricted_use_names. "
                                               f"They are currently: {restricted_use_names}")
        if name[-1] == "?":
            raise ButtonNameSyntaxError(f"Button name {name} can't end in '?'")

        restricted_use_names.append(name)

        self.page.all_button_names.append(self.name)

        if previous_name is not None:
            self.page.all_button_names.remove(previous_name)

            button_has_function = previous_name in self.page.website.buttons_with_functions

            if button_has_function:
                # update name in dictionary of button names and functions
                self.page.website.buttons_with_functions.pop(previous_name)
                self.page.website.buttons_with_functions[self.name]: Button = self

    @property
    def button_link(self):
        return self._button_link

    @button_link.setter
    def button_link(self, link):
        if link is None:
            self._button_link = link
        else:
            self._button_link = format_url(link)

    @property
    def button_html(self):
        """ Return the html text for adding this button.

        Returns
        -------
        str

        """
        return f"\n\t<div class='button-container'>" \
               f"<button onclick='performAction{self.name}()'>{self.text}</button></div>"

    @property
    def button_function_script(self):
        button_function_script = f"\n" \
                                 f"\t\tfunction performAction{self.name}() {{\n" \
                                 f"\t\t\tfetch('/{self.name}')\n" \
                                 f"\t\t\t\t.then(response => response.text())\n" \
                                 f"\t\t}}\n" \
                                 f"\n"
        return button_function_script

    @property
    def button_link_script(self):
        button_link_script = f"\n" \
                             f"\t\tfunction performAction{self.name}() {{\n" \
                             f"\t\t\twindow.location.href = \"{self.button_link}\";" \
                             f"\t\t}}\n" \
                             f"\n"
        return button_link_script

    def build(self):
        """ Add html and css for the buttons to files for website generation.

        """
        with open(self.page.html_part2_path, "a") as f:
            f.write(self.button_html)

        button_has_function = self.button_function is not None
        if button_has_function:
            with open(self.page.html_part4_path, "a") as f:
                f.write(self.button_function_script)

        button_has_link = self.button_link is not None
        if button_has_link:
            with open(self.page.html_part4_path, "a") as f:
                f.write(self.button_link_script)
