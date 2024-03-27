from __future__ import annotations

from .exceptions import DuplicateNameError

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ._page import Page
    from .settings_objects import ButtonSettings


class Button:
    """ A button and all its information

        Attributes
        ----------
        settings: ButtonSettings
            The settings object containing all the changeable settings for the button

        """

    def __init__(self, page: Page, settings: ButtonSettings):
        self.settings = settings

        self.page: Page = page
        self.color_class = ""

        while True:
            generated_name = self.page.website.button_name_generator.generate()
            try:
                self.settings.check_if_name_restricted_and_add(generated_name)
                break
            except DuplicateNameError:
                continue

        self.name: str = generated_name

    @property
    def button_html(self):
        return f"\n\t<div class='button-container'>" \
               f"<button {self.color_class}onclick='performAction{self.name}()'>{self.settings.text}</button></div>"

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
                             f"\t\t\twindow.location.href = \"{self.settings.link}\";" \
                             f"\t\t}}\n" \
                             f"\n"
        return button_link_script

    def build(self):

        self.settings.check_required_settings()

        button_has_default_color = self.settings.color == "default"
        if not button_has_default_color:
            self.color_class = self.page.button_colors_and_classes[self.settings.color]
            self.color_class = f"class={self.color_class} "

        self.page.html_part_2 += self.button_html

        button_has_function = self.settings.function is not None
        if button_has_function:
            self.page.html_part_4 += self.button_function_script

        button_has_link = self.settings.link is not None
        if button_has_link:
            self.page.html_part_4 += self.button_link_script


