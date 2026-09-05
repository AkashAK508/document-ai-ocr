import re

from utils.text_utils import normalize_text


def is_noise_line(line):
    line = line.strip()

    if not line:
        return True

    if not re.search(r"[A-Za-z0-9]", line):
        return True

    if re.fullmatch(r"[\(\[\{]?[A-Za-z0-9]{1,3}[\)\]\}]?", line):
        return True

    if re.fullmatch(r"[-\_=:.|]+", line):
        return True

    return False


def is_field_label(line):
    line = line.strip()

    if not line:
        return False

    if line.endswith(":"):
        return True

    if re.match(r"^[\(\[\{]?[A-Za-z0-9]+[\)\]\}]?", line):
        return True

    return False


def keyword_matches_line(line, keyword):
    normalized_line = normalize_text(line)
    normalized_keyword = normalize_text(keyword)

    if normalized_keyword in normalized_line:
        return True

    keyword_words = normalized_keyword.split()
    line_words = normalized_line.split()

    if len(keyword_words) == 1:
        keyword_word = keyword_words[0]

        for word in line_words:
            if word.startswith(keyword_word):
                return True

    compact_line = re.sub(r"[^a-z0-9]", "", normalized_line)
    compact_keyword = re.sub(r"[^a-z0-9]", "", normalized_keyword)

    if compact_keyword in compact_line:
        return True

    return False


def extract_value_from_line(line, keyword):
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    match = pattern.search(line)

    if match:
        value = line[match.end():].strip()
        value = value.lstrip(" :-–—|")

        if value and not is_noise_line(value):
            return value

    compact_keyword = re.sub(r"[^A-Za-z0-9]", "", keyword)

    if compact_keyword:
        spaced_pattern = r"\s\*".join(re.escape(char) for char in compact_keyword)
        pattern = re.compile(spaced_pattern, re.IGNORECASE)
        match = pattern.search(line)

        if match:
            value = line[match.end():].strip()
            value = value.lstrip(" :-–—|")

            if value and not is_noise_line(value):
                return value

    return None


def find_keyword_content(page_text, keyword):
    lines = page_text.splitlines()
    candidate_indexes = []

    for index, line in enumerate(lines):
        clean_line = line.strip()

        if is_noise_line(clean_line):
            continue

        if keyword_matches_line(clean_line, keyword):
            candidate_indexes.append(index)

    if not candidate_indexes:
        return None

    for index in candidate_indexes:
        current_line = lines[index].strip()

        same_line_value = extract_value_from_line(current_line, keyword)

        if same_line_value:
            return same_line_value

        collected = []

        for next_index in range(index + 1, min(index + 8, len(lines))):
            next_line = lines[next_index].strip()

            if is_noise_line(next_line):
                continue

            if is_field_label(next_line) and not collected:
                continue

            if is_field_label(next_line) and collected:
                break

            collected.append(next_line)

            if len(collected) >= 2:
                break

        if collected:
            value = " ".join(collected)
            value = value.strip()

            if value:
                return value

    for index in candidate_indexes:
        current_line = lines[index].strip()

        if len(current_line.split()) > 1:
            return current_line

    return None


def search_document(pages_text, keyword):
    findings = []

    for page_number, page_text in enumerate(pages_text, start=1):
        result = find_keyword_content(page_text, keyword)

        if result:
            findings.append({
                "page": page_number,
                "value": result
            })

    return findings