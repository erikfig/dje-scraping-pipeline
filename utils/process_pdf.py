import os
import requests
import hashlib
from PyPDF2 import PdfReader

HEADERS = {"User-Agent": "Mozilla/5.0"}

def process_pdf(url):
    response = requests.get(url, headers=HEADERS)
    filename = hashlib.md5(url.encode()).hexdigest()

    with open(f"{filename}.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)

    reader = PdfReader(f"{filename}.pdf")
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        full_text += text
  
    os.remove(f"{filename}.pdf")

    return full_text
