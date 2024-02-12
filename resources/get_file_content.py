from pypdf import PdfReader

def get_txt_file_content(file_path : str) -> str:
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content


def get_pdf_file_content(file_path : str) -> str:
    pdf_file = open(file_path, 'rb')
    pdf_reader = PdfReader(pdf_file)

    pdf_content = ''
    for page in pdf_reader.pages:
        pdf_content += page.extract_text()

    pdf_file.close()

    return pdf_content