import re

def clean_text(text: str) -> str:
    """Clean webpage text before embedding."""

    # normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # remove chatbot widget
    text = re.sub(r"Hello! I'm Leadsy.*?", "", text)

    # remove navigation sections
    patterns = [
        r"Services.*?Products",
        r"Products.*?Certification",
        r"Site Links.*",
    ]

    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return text.strip()

from bs4 import BeautifulSoup

