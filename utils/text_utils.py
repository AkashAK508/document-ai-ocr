import re


def normalize_text(text):
    return re.sub(r"\s+", "", text).lower()


def normalize_for_search(text):
    return re.sub(r"\s+", " ", text).strip()