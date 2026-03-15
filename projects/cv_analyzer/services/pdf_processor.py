import PyPDF2
from io import BytesIO


def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
        text = ""
        for number_page, page in enumerate(pdf_reader.pages, 1):
            page_text = page.extract_text()
            if page_text.strip():
                text += f"\n--- Página {number_page} ---\n{page_text}"


        text = text.strip()
        if not text:
            return "No se pudo extraer texto del PDF"
        return text
    except Exception as e:
        print(f"Error al extraer texto del PDF: {e}")
        return "No se pudo extraer texto del PDF"
