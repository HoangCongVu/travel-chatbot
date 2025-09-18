from urllib.request import Request, urlopen
from io import StringIO
import csv

url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"

def readCsv(url: str) -> str:
    try:
        remote_file = urlopen(Request(url)).read()
        text_data = remote_file.decode("utf-8")
        return text_data
    except Exception as e:
        print("ERROR:", e)
        return "Failed to load content"

# Gọi hàm để lấy text CSV
csv_text = readCsv(url)