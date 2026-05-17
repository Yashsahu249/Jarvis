import re


def detect_language(text: str) -> str:
    if not text.strip():
        return "unknown"

    hindi_chars = re.findall(r"[\u0900-\u097F]", text)
    english_chars = re.findall(r"[a-zA-Z]", text)

    total = len(hindi_chars) + len(english_chars)
    if total == 0:
        return "unknown"

    hindi_ratio = len(hindi_chars) / total if total > 0 else 0

    if hindi_ratio > 0.7:
        return "hindi"
    elif hindi_ratio > 0.1:
        return "hinglish"
    else:
        return "english"
