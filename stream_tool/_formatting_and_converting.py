from .exceptions import InvalidColorValueError


def convert_to_pascal_case(string: str):
    string = string.replace("-", " ")
    string = string.replace("_", " ")
    if ' ' in string:
        string = string.title()
        string = string.replace(" ", "")
    else:
        string = string[0].capitalize() + string[1:]
    return string


def format_url(url: str):
    url_is_formatted = url.startswith("http://") or url.startswith("https://") or url.startswith("/")
    if url_is_formatted:
        return url
    else:
        return f"http://{url}"


def format_page_name(page_name: str):
    page_name = page_name.replace(" ", "-")
    page_name = page_name.replace("_", "-")
    return page_name


def format_and_check_color(color: str):
    valid_css_colors = ["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive",
                        "purple", "red", "silver", "teal", "white", "yellow"]
    valid_hex_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    color = color.lower()
    if color in valid_css_colors:
        return color
    else:
        if color[0] != "#":
            color = f"#{color}"
        color = color.upper()
        if len(color) != 7:
            raise InvalidColorValueError(f"The color name or hex supplied ({color}) is not valid in css")
        for i in range(1, 7):
            if color[i] not in valid_hex_characters:
                raise InvalidColorValueError
        return color
