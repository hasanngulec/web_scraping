def url_to_filename(url: str) -> str:
    """
    Converts a URL into a safe filename.
    """
    return url.replace("://", "_").replace("/", "_") + ".html" 