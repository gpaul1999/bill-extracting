import io
import pdfplumber
from PIL import Image
import pytesseract


def parse_pdf(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def parse_image(file_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(image)


def parse_file(filename: str, file_bytes: bytes) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        return parse_pdf(file_bytes)
    elif ext in ("png", "jpg", "jpeg", "webp", "tiff", "bmp"):
        return parse_image(file_bytes)
    raise ValueError(f"Unsupported file type: {ext}")
