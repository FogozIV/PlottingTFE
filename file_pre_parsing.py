import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os


def ocr_from_pdf(pdf_path, dpi=300, lang="eng"):
    print(f"Converting PDF: {pdf_path}")
    pages = convert_from_path(pdf_path, dpi=dpi)

    extracted_text = ""
    for i, page in enumerate(pages):
        print(f"Processing page {i + 1}/{len(pages)}...")
        text = pytesseract.image_to_string(page, lang=lang)
        extracted_text += f"\n--- Page {i + 1} ---\n{text}\n"

    return extracted_text


def ocr_from_image(image_path, lang="eng"):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, lang=lang)


# Example usage:
if __name__ == "__main__":
    # For PDF
    pdf_text = ocr_from_pdf("test.pdf")
    with open("ocr_output.txt", "w", encoding="utf-8") as f:
        f.write(pdf_text)

    # Or for a single image:
    # text = ocr_from_image("your_image.jpg")
    # print(text)