import pytesseract
from PIL import Image


def extract_text_from_image(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise Exception(f"OCR failed: {e}")


def extract_text_from_page(page):
    try:
        pixmap = page.get_pixmap(matrix=__import__("fitz").Matrix(2, 2))

        image = Image.frombytes(
            "RGB",
            [pixmap.width, pixmap.height],
            pixmap.samples
        )

        return extract_text_from_image(image)

    except Exception as e:
        raise Exception(f"PDF page OCR failed: {e}")