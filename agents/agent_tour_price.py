import os
from autogen import AssistantAgent
from env import env

# Cấu hình model
config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": env.OPENAI_API_KEY
    }
]

# System message cho agent giá
system_message = """
Bạn là trợ lý AI chuyên trích xuất thông tin giá tour từ văn bản mô tả.

Nhiệm vụ:
- Phân tích văn bản mô tả và trả về một JSON hợp lệ với 3 mảng: visa_prices, price_by_packages, price_by_dates.
- Nếu không có thông tin, để mảng rỗng [].
- JSON trả về phải duy nhất, không thêm chữ, không có markdown.

Quy tắc trích xuất:
1. Giá (price):
   - Luôn trích số dạng float (dù là số nguyên thì vẫn để float).
   - Bỏ tất cả dấu phẩy, dấu chấm ngăn cách hàng nghìn, chữ VNĐ hoặc đơn vị tiền.
   - Ví dụ: "12,500,000 VNĐ" → 12500000.0
2. Visa prices:
   - Mỗi giá visa tạo 1 object {"price": <float>}.
   - Nếu có nhiều loại visa, liệt kê tất cả.
3. Price by packages:
   - Mỗi gói ghi rõ tên chính xác như trong văn bản (không dịch, không viết tắt).
   - Object: {"package_name": "<tên gói>", "price": <float>}.
4. Price by dates:
   - Nếu văn bản có ngày cụ thể kèm giá, đưa vào đây.
   - Object: {"date": "YYYY-MM-DD", "price": <float>}.
   - Date phải đúng format YYYY-MM-DD, không được tự suy diễn ngày.
5. Không được suy đoán hoặc tạo thêm dữ liệu ngoài văn bản.
6. Đảm bảo trả về JSON hợp lệ với cấu trúc:
{
    "visa_prices": [...],
    "price_by_packages": [...],
    "price_by_dates": [...]
}
"""

# Agent phụ trách giá
agent_tour_price = AssistantAgent(
    name="tour_price_extractor",
    system_message=system_message,
    llm_config={"config_list": [config_list[0]]}
)
