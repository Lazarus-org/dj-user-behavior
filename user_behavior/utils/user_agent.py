import re
from typing import Tuple


def detect_browser(user_agent: str) -> Tuple[str, str]:
    """
    Detects the browser name and version from the User-Agent string.

    Args:
        user_agent (str): The user agent string to parse.

    Returns:
        Tuple[str, str]: A tuple containing the browser name and version.
    """
    browsers = [
        ("Edge", r"Edg/([\d.]+)"),
        ("Opera", r"OPR/([\d.]+)"),
        ("Chrome", r"CriOS/([\d.]+)"),
        ("Chrome", r"Chrome/([\d.]+)"),
        ("Firefox", r"Firefox/([\d.]+)"),
        ("Safari", r"Version/([\d.]+).*Safari"),
        ("Internet Explorer", r"MSIE ([\d.]+);"),
        ("Internet Explorer", r"Trident/.*rv:([\d.]+)"),
    ]

    for name, pattern in browsers:
        match = re.search(pattern, user_agent)
        if match:
            return name, match.group(1)

    return "Unknown", "0.0"
