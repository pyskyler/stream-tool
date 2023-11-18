
def convert_to_pascal_case(string: str):
    string = string.title()
    string = string.replace(" ", "")
    return string


def format_url(url: str):
    url_is_formatted = url.startswith("http://") or url.startswith("https://")
    if url_is_formatted:
        return url
    else:
        return f"http://{url}"
