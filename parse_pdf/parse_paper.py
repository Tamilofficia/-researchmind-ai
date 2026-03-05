import fitz  # PyMuPDF

def parse_pdf(file):

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    return text
    