from config.document_patterns import DOCUMENT_PATTERNS, MINIMUM_MATCH_PERCENTAGE
from utils.text_utils import normalize_text


def identify_document(text):
    normalized_document = normalize_text(text)

    scores = {}
    matched_parameters = {}
    percentages = {}

    for category, patterns in DOCUMENT_PATTERNS.items():
        matches = []

        for pattern in patterns:
            normalized_pattern = normalize_text(pattern)

            if normalized_pattern in normalized_document:
                matches.append(pattern)

        total_patterns = len(patterns)
        matched_count = len(matches)
        match_percentage = (matched_count / total_patterns) * 100

        scores[category] = matched_count
        percentages[category] = round(match_percentage, 2)
        matched_parameters[category] = matches

    ranked = sorted(percentages.items(), key=lambda x: x[1], reverse=True)

    best_category = ranked[0][0]
    best_percentage = ranked[0][1]
    second_percentage = ranked[1][1] if len(ranked) > 1 else 0

    best_matched_count = scores[best_category]
    total_patterns = len(DOCUMENT_PATTERNS[best_category])

    if best_percentage < MINIMUM_MATCH_PERCENTAGE:
        return {
            "category": "UNRECOGNIZED",
            "match_percentage": best_percentage,
            "matched_count": best_matched_count,
            "total_patterns": total_patterns,
            "matched": matched_parameters[best_category],
            "score": best_percentage,
            "message": "Document could not be reliably identified."
        }

    if best_percentage == second_percentage:
        return {
            "category": "UNRECOGNIZED",
            "match_percentage": best_percentage,
            "matched_count": best_matched_count,
            "total_patterns": total_patterns,
            "matched": matched_parameters[best_category],
            "score": best_percentage,
            "message": "Document matches multiple document categories."
        }

    return {
        "category": best_category,
        "match_percentage": best_percentage,
        "matched_count": best_matched_count,
        "total_patterns": total_patterns,
        "matched": matched_parameters[best_category],
        "score": best_percentage,
        "message": f"Most likely document is {best_category}."
    }