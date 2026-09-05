import fitz
from extraction.ocr_reader import extract_text_from_page


def is_blank_page(page):
    text = page.get_text("text").strip()

    if text:
        return False

    if page.get_images(full=True):
        return False

    if page.get_drawings():
        return False

    return True


def extract_pdf(pdf_path):
    try:
        pdf = fitz.open(pdf_path)
    except Exception as e:
        raise Exception(f"Unable to open PDF: {e}")

    if len(pdf) == 0:
        pdf.close()
        raise Exception("PDF contains no pages.")

    pages_text = []
    blank_pages = 0

    for page in pdf:
        if is_blank_page(page):
            blank_pages += 1
            pages_text.append("")
            continue

        text = page.get_text("text").strip()

        if not text:
            print("  OCR processing scanned page...")
            text = extract_text_from_page(page)

        pages_text.append(text)

    total_pages = len(pdf)
    pdf.close()

    return {
        "pages_text": pages_text,
        "total_pages": total_pages,
        "blank_pages": blank_pages
    }