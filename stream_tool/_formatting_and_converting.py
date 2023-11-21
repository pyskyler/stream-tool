
def convert_to_pascal_case(string: str):
    string = string.title()
    string = string.replace(" ", "")
    return string


def format_url(url: str):
    url_is_formatted = url.startswith("http://") or url.startswith("https://") or url.startswith("/")
    if url_is_formatted:
        return url
    else:
        return f"http://{url}"


def format_page_name(page_name: str):
    page_name = page_name.replace(" ", "-")
    return page_name
