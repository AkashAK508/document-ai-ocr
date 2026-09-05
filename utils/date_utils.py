import re


def extract_date(first_page_text):
    patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b\d{1,2}[-/ ](?:January|February|March|April|May|June|July|August|September|October|November|December)[-/ ]\d{4}\b",
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
        r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, first_page_text, re.IGNORECASE)

        if match:
            return match.group()

    year = re.search(r"\b(?:19|20)\d{2}\b", first_page_text)

    if year:
        return year.group()

    month = re.search(
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b",
        first_page_text,
        re.IGNORECASE
    )

    if month:
        return month.group()

    return "No mentioned"