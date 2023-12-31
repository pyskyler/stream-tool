from __future__ import annotations

from ._formatting_and_converting import convert_to_pascal_case, format_url
from .exceptions import DuplicateButtonNameError, ButtonNameSyntaxError

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ._page import Page


class Button:
    """ A button and all its information

        Attributes
        ----------
        name: str
            The name of the button
        text: str
            Text for the button, defaults to the name parameter
        color: str
            Color of the button, defaults to "defualt" which is blue. Set it to a valid css color
            name or a valid rgb hex color.
        button_function: callable
            Action for button to run on press
        button_function_args: list, Any
            Arguments or single argument to be passed to button_function
        button_function_kwargs: dict,
            Keyword arguments to be passed to button_function
        button_link: str
            A url to a relative page on the site or any page on the web

        """

    def __init__(self, page: Page, name: str, button_function: callable = None, button_function_args: list = None,
                 button_function_kwargs: dict = None, text: str = None, button_link: str = None,
                 color: str = "default"):
        self._button_function = None
        self.page: Page = page
        self._name = None
        self.name: str = name
        if text is None:
            self.text = self.name
        else:
            self.text = text
        self.button_function = button_function
        self._button_function_args = None
        self.button_function_args = button_function_args
        self._button_function_kwargs = None
        self.button_function_kwargs = button_function_kwargs
        self.button_link = button_link
        self.color = color
        self.color_class = ""

    @property
    def button_function(self):
        return self._button_function

    # TODO: could this just be some kind of dict comprehension? or a property on page
    #  that finds all the functional buttons?
    @button_function.setter
    def button_function(self, function):
        self._button_function = function
        if self.button_function is not None:
            self.page.website.buttons_with_functions[self.name]: Button = self

    @property
    def button_function_args(self):
        return self._button_function_args

    @button_function_args.setter
    def button_function_args(self, args):
        if args is not None:
            if isinstance(args, list):
                self._button_function_args = args
            else:
                self._button_function_args = [args]
        else:
            self._button_function_args = []

    @property
    def button_function_kwargs(self):
        return self._button_function_kwargs

    @button_function_kwargs.setter
    def button_function_kwargs(self, kwargs):
        if kwargs is not None:
            if isinstance(kwargs, dict):
                self._button_function_kwargs = kwargs
            else:
                self._button_function_kwargs = dict([kwargs])
        else:
            self._button_function_kwargs = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        previous_name = self.name
        name = convert_to_pascal_case(name)
        self._name = name

        if name in self.page.website.restricted_use_names:
            if name in self.page.all_button_names:
                raise DuplicateButtonNameError(f"Button name {name} already in use. Use a different name.")
            else:
                raise DuplicateButtonNameError(f"Button name {name} is not allowed to be used. Use a different name. "
                                               f"Restricted use names are in list website.restricted_use_names. "
                                               f"They are currently: {self.page.website.restricted_use_names}")
        if name[-1] == "?":
            raise ButtonNameSyntaxError(f"Button name {name} can't end in '?'")

        self.page.website.restricted_use_names.append(name)

        # TODO: Does this removing and adding every time a name changes need to exist or can
        #  the list just be created later with a list comprehension (or a dict comprehension)?
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
        return f"\n\t<div class='button-container'>" \
               f"<button {self.color_class}onclick='performAction{self.name}()'>{self.text}</button></div>"

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
        button_has_default_color = self.color == "default"
        if not button_has_default_color:
            self.color_class = self.page.button_colors_and_classes[self.color]
            self.color_class = f"class={self.color_class} "

        self.page.html_part_2 += self.button_html

        button_has_function = self.button_function is not None
        if button_has_function:
            self.page.html_part_4 += self.button_function_script

        button_has_link = self.button_link is not None
        if button_has_link:
            self.page.html_part_4 += self.button_link_script


