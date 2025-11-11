import os
import requests
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def general_web_search(query: str, num_results: int = 5):
    """
    Tìm kiếm thông tin thời gian thực qua Serper.dev (Google Search wrapper)
    Trả về danh sách {title, link, snippet} và bản tóm tắt ngắn.
    
    Args:
        query: Từ khóa tìm kiếm
        num_results: Số kết quả tối đa (mặc định 5)
        
    Returns:
        Dict chứa query, summary và sources
    """
    if not SERPER_API_KEY:
        raise ValueError("Thiếu SERPER_API_KEY. Đăng ký tại https://serper.dev và set biến môi trường này.")

    url = "https://google.serper.dev/search"
    payload = {"q": query, "num": num_results}
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {"error": f"Lỗi gọi Serper API: {e}"}

    results = data.get("organic", [])
    sources = []
    for r in results[:num_results]:
        sources.append({
            "title": r.get("title"),
            "url": r.get("link"),
            "snippet": r.get("snippet", "")
        })

    # Ghép tóm tắt sơ bộ
    summary_text = "\n".join([r["snippet"] for r in sources if r.get("snippet")])
    summary_text = summary_text[:2000] if summary_text else "Không tìm thấy thông tin phù hợp."

    return {
        "query": query,
        "summary": summary_text,
        "sources": sources
    }
