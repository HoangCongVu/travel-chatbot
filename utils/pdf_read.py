import re
from urllib.request import Request, urlopen
from PyPDF2 import PdfReader
from io import BytesIO

def extract_file_id(drive_url: str) -> str:
    """
    Trích xuất file ID từ URL Google Drive.
    """
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', drive_url)
    if match:
        return match.group(1)
    raise ValueError("Không thể tìm thấy file ID trong URL.")

def get_direct_download_url(drive_url: str) -> str:
    """
    Tạo URL tải trực tiếp từ URL Google Drive.
    """
    file_id = extract_file_id(drive_url)
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def readPdf(url: str) -> str:
    """
    Đọc nội dung từ file PDF tại URL, bao gồm Google Drive file URL.
    """
    content = ""

    # Nếu là link Google Drive, tạo link tải trực tiếp
    if "drive.google.com" in url:
        url = get_direct_download_url(url)

    # Gửi request và đọc dữ liệu PDF
    remoteFile = urlopen(Request(url)).read()
    memoryFile = BytesIO(remoteFile)

    # Đọc file PDF
    pdfFile = PdfReader(memoryFile)

    # Trích xuất nội dung từng trang
    for page in pdfFile.pages:
        text = page.extract_text()
        if text:
            content += text + "\n"
    return content