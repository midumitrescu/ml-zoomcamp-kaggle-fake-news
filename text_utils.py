import re

# Characters to remove from title/text
CLEANUP_REGEX = r"[()\\\/:;'@.,!?\u2018\u2019\u201c\u201d-]"

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(CLEANUP_REGEX, " ", text)
    text = text.replace(" -", "").replace("-", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text
