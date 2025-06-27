import fitz  # PyMuPDF
from werkzeug.utils import secure_filename


def extract_text_from_pdf(pdf_path):
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)

        text = ""
        for page in doc:
            text += page.get_text()

        doc.close()
        return text.strip()

    except Exception as e:
        print(f"⚠️ Error reading PDF: {e}")
        return ""

# print(extract_text_from_pdf('23sc06007_REEP_Report.pdf'))