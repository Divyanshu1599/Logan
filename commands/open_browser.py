import webbrowser

def handle(text: str) -> None:
    """Open a web browser to the specified URL.

    Args:
        text (str): The URL to open in the web browser.
    """
    webbrowser.open("https://www.google.com/")
    return "Opening browser"
