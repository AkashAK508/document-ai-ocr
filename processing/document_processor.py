import os

from extraction.pdf_reader import extract_pdf
from classification.document_classifier import identify_document
from utils.date_utils import extract_date


def process_document(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")

    print(f"\nProcessing: {os.path.basename(pdf_path)}")

    pdf_data = extract_pdf(pdf_path)
    pages_text = pdf_data["pages_text"]
    complete_text = "\n".join(pages_text)

    classification = identify_document(complete_text)
    date = extract_date(pages_text[0])

    return {
        "path": pdf_path,
        "name": os.path.basename(pdf_path),
        "type": classification["category"],
        "score": classification["score"],
        "matched": classification["matched"],
        "date": date,
        "pages": pdf_data["total_pages"],
        "blank_pages": pdf_data["blank_pages"],
        "pages_text": pages_text
    }