import os
from autogen import AssistantAgent
from env import env

# Cấu hình model
config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": env.OPENAI_API_KEY,
    }
]

# System message cho agent phụ trách tour_type_id
tour_type_message = """
Bạn là một trợ lý AI chuyên trích xuất loại tour từ mô tả tour du lịch.

Nhiệm vụ:
1. Đọc kỹ văn bản và suy luận loại tour dựa trên ngữ cảnh (điểm đi, điểm đến, hình thức tổ chức, loại dịch vụ).
2. Chọn duy nhất một loại tour phù hợp trong bảng sau và trả về đúng cặp tour_type_id và tour_type_name:

    1: Tour trong nước (nội địa)
    2: Tour quốc tế (nước ngoài)
    3: Tour trong ngày
    4: Combo du lịch (gói dịch vụ)
    5: Team building
    6: MICE (du lịch hội nghị, hội thảo)
    7: Free & Easy (vé máy bay + khách sạn)

Quy định:
- Luôn phải suy luận để gán tour vào một trong các loại trên, không được bỏ trống hoặc mặc định.
- Chỉ trả về duy nhất một JSON hợp lệ, không có giải thích, không markdown, không văn bản thừa.
- tour_type_id và tour_type_name phải khớp chính xác một trong các giá trị đã cho.
"""

# System message cho agent chính
tour_system_message = """
Bạn là một trợ lý AI chuyên trích xuất thông tin tour du lịch từ văn bản mô tả.

Nhiệm vụ:
- Phân tích văn bản và chỉ trả về duy nhất một đối tượng JSON hợp lệ theo cấu trúc sau:
{
  "tour_name": "string",
  "days": integer,
  "description": "string",
  "highlight": "string",
  "itinerary_url": "string",
  "detail_url": "string",
  "promotion_info": "string",
  "price_type": "string"
}

Quy tắc trích xuất:
1. tour_name:
   - Tên tour (bắt buộc, không để trống).
   - Nếu không có thông tin tên tour, sử dụng tiêu đề hoặc cụm mô tả chính.

2. days:
   - Số ngày của tour (kiểu số nguyên).
   - Nếu văn bản có thông tin dạng "X ngày Y đêm" → lấy X.
   - Nếu không có thông tin rõ ràng, phải cố gắng suy luận từ ngữ cảnh.

3. Các trường còn lại:
   - description, highlight, itinerary_url, detail_url, promotion_info: 
     nếu không có trong văn bản → để giá trị rỗng "".

4. price_type:
   - Chỉ nhận một trong ba giá trị sau:
       "Một giá" → nếu văn bản chỉ nêu một giá duy nhất.
       "Phụ thuộc ngày khởi hành" → nếu giá thay đổi theo ngày hoặc lịch khởi hành.
       "Phụ thuộc gói" → nếu có nhiều gói dịch vụ/loại vé khác nhau với các mức giá riêng.
   - Nếu không xác định được → mặc định là "Một giá".

5. Không được tự tạo hoặc suy đoán dữ liệu ngoài văn bản (ngoại trừ việc lấy số ngày từ cụm "X ngày Y đêm").

6. Chỉ trả về JSON hợp lệ, không có chú thích, không có Markdown, không có văn bản ngoài JSON.
"""

# Agent phụ trách price_type và tour_type_id
agent_tour_type = AssistantAgent(
    name="agent_tour_type",
    system_message=tour_type_message,
    llm_config={
        "config_list": [config_list[0]], 
    }
)

# Agent chính trích xuất toàn bộ thông tin tour
agent_tour = AssistantAgent(
    name="agent_tour",
    system_message=tour_system_message,
    llm_config={
        "config_list": [config_list[0]], 
    }
)