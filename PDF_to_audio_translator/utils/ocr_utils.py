# utils/ocr_utils.py

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfReader

# Path for Windows Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(file_path, lang="eng"):
    """
    Try extracting text directly. If not enough, run OCR.
    """
    text = ""

    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    except:
        text = ""

    if len(text.strip()) < 50:
        text = ocr_pdf(file_path, lang=lang)

    return text.strip()


def ocr_pdf(file_path, dpi=300, lang="eng", poppler_path=None):
    images = convert_from_path(file_path, dpi=dpi, poppler_path=poppler_path)
    out_text = []

    for img in images:
        if img.mode != "RGB":
            img = img.convert("RGB")
        txt = pytesseract.image_to_string(img, lang=lang)
        out_text.append(txt)

    return "\n".join(out_text)


def ocr_image(image_path, lang="eng"):
    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    return pytesseract.image_to_string(img, lang=lang)
