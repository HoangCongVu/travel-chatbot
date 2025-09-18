import requests
from io import BytesIO, StringIO
from PyPDF2 import PdfReader
from docx import Document
import csv

def download_bytes(url: str) -> bytes:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content

def readFileFromUrl(url: str) -> str:
    data = download_bytes(url)

    # PDF: bắt đầu bằng %PDF
    if data.startswith(b"%PDF"):
        pdf = PdfReader(BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

    # DOCX: file zip -> bắt đầu bằng PK
    if data.startswith(b"PK"):
        doc = Document(BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs if p.text)

    # CSV hoặc text
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin1", errors="ignore")

    # nếu có dấu phẩy và nhiều dòng -> coi như CSV
    if "," in text and "\n" in text:
        reader = csv.reader(StringIO(text))
        return "\n".join([", ".join(row) for row in reader])
    return text
