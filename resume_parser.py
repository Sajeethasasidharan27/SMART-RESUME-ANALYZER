import docx2txt
from pdfminer.high_level import extract_text as pdf_extract

def extract_text(filepath):
    try:
        lower_path = filepath.lower()
        if lower_path.endswith('.pdf'):
            return pdf_extract(filepath) or ''
        elif lower_path.endswith('.docx'):
            return docx2txt.process(filepath) or ''
    except Exception:
        return ''
    return ''
