import os
from urllib.parse import quote

def generate_vietqr(amount: int, content: str) -> str:
    """
    Tạo VietQR URL hợp lệ
    """
    bank_bin = os.getenv("BANK_BIN")
    account_no = os.getenv("BANK_ACCOUNT_NO")
    account_name = os.getenv("BANK_ACCOUNT_NAME")

    # content cần encode, nhưng account name KHÔNG encode
    encoded_content = quote(content)

    qr_url = (
        f"https://img.vietqr.io/image/{bank_bin}-{account_no}-compact.jpg"
        f"?amount={amount}"
        f"&addInfo={encoded_content}"
        f"&accountName={account_name}"
    )

    return qr_url
