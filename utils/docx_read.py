import re
from urllib.request import Request, urlopen
from io import BytesIO
from docx import Document

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

def readDocx(url: str) -> str:
     """
     Đọc nội dung từ file DOCX tại URL, bao gồm Google Drive file URL.
     """
     content = ""

     # Nếu là link Google Drive, tạo link tải trực tiếp
     if "drive.google.com" in url:
         url = get_direct_download_url(url)

     # Gửi request và đọc dữ liệu DOCX
     remoteFile = urlopen(Request(url)).read()
     memoryFile = BytesIO(remoteFile)

     # Đọc file DOCX
     doc = Document(memoryFile)

     # Trích xuất nội dung từng đoạn
     for para in doc.paragraphs:
         content += para.text + "\n"
    
     return content