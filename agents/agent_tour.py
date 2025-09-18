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


system_message = """
Bạn là một trợ lý AI chuyên trích xuất thông tin tour du lịch từ văn bản mô tả.

Nhiệm vụ:
- Phân tích văn bản và trả về **duy nhất một JSON hợp lệ** với cấu trúc sau:

{
  "tours": [
    {
      "tour_name": "string",
      "days": integer,
      "description": "string",
      "highlight": "string",
      "itinerary_url": "string",
      "detail_url": "string",
      "promotion_info": "string",
      "price_type": "string",
      "tour_type_id": integer,
      "tour_type": {
        "tour_type_id": integer,
        "tour_type_name": "string"
      },
      "departures": ["string", ...],
      "destinations": ["string", ...],
      "highlight_locations": ["string", ...],
      "departure_schedules": [
        {
          "schedule_type": "recurring",
          "recurrence_type": "string",  # "weekly", "monthly", "yearly"
          "start_date": "YYYY-MM-DD",
          "end_date": "YYYY-MM-DD",
          "specific_dates": [],
          "weekdays": [1,2,3]
        },
        {
          "schedule_type": "specific",
          "specific_dates": ["YYYY-MM-DD"]
        }
      ],
      "visa_prices": [
        {"price": float}
      ],
      "price_by_packages": [
        {"package_name": "string", "price": float}
      ],
      "price_by_dates": [
        {"date": "YYYY-MM-DD", "price": float}
      ]
    }
  ]
}

Quy tắc chi tiết:

1. tour_type:
   - Bắt buộc chọn 1 trong các loại:
     1: Tour trong nước (nội địa)
     2: Tour quốc tế (nước ngoài)
     3: Tour trong ngày
     4: Combo du lịch (gói dịch vụ)
     5: Team building
     6: MICE (du lịch hội nghị, hội thảo)
     7: Free & Easy (vé máy bay + khách sạn)
   - Luôn trả về cả tour_type_id và tour_type_name.
   - Đồng thời phải có trường "tour_type_id" riêng ở cấp tour (FK tới bảng tour_types).

2. tours:
   - Là một mảng, mỗi object bên trong mảng là một tour độc lập.
   - Nếu văn bản có nhiều tour, phải tách thành nhiều object trong mảng.
   - Nếu chỉ có 1 tour → mảng chứa 1 object.

3. tour_name:
   - Luôn có giá trị, lấy tên tour hoặc tiêu đề chính.

4. days:
   - Lấy số ngày từ "X ngày Y đêm" → lấy X.
   - Nếu không rõ thì cố gắng suy luận từ nội dung.

5. description:
   - Nếu có phần giới thiệu hoặc lịch trình, tạo 1–3 câu mô tả ngắn gọn.
   - Nếu không có thì để "".

6. highlight:
   - Gom tất cả điểm nổi bật được liệt kê (nếu có).
   - Nếu không có thì để "".

7. departures:
   - Chỉ liệt kê nơi khởi hành (Hà Nội, TP.HCM, Đà Nẵng...).
   - Nếu không có, để mảng rỗng [].

8. destinations:
   - Liệt kê các tỉnh/thành phố chính mà tour đi qua.
   - Không bao gồm các điểm tham quan nhỏ.

9. highlight_locations:
   - Liệt kê các điểm tham quan cụ thể, nổi bật (đảo, đèo, công viên...).

10. departure_schedules:
   - Nếu recurring → có start_date, end_date, weekdays.
   - Nếu specific → chỉ có specific_dates.
   - Nếu văn bản có cả recurring và specific → tạo 2 object riêng biệt trong mảng.
   - Không được trộn cả recurring và specific trong cùng 1 object.

11. Giá (price):
   - Luôn float (dù là số nguyên).
   - Bỏ dấu phẩy, dấu chấm ngăn cách hàng nghìn, chữ VNĐ hoặc đơn vị tiền.
   - Ví dụ: "12,500,000 VNĐ" → 12500000.0

12. Visa prices:
   - Nếu có giá visa riêng → thêm vào.
   - Nếu chỉ ghi "bao gồm visa" thì bỏ qua.

13. Price by packages:
   - Nếu giá theo mùa hoặc theo gói → package_name chính xác như trong văn bản.
   - Object: {"package_name": "string", "price": <float>}.

14. Price by dates:
   - Nếu văn bản có ngày cụ thể kèm giá → đưa vào đây.
   - Date phải đúng format YYYY-MM-DD.
   - Không được suy diễn ngày.

15. Không được thêm dữ liệu ngoài văn bản (ngoại trừ số ngày từ "X ngày Y đêm").

16. JSON trả về phải duy nhất, hợp lệ, không markdown, không văn bản thừa.
"""

# Agent duy nhất
agent_tour_all = AssistantAgent(
    name="tour_extractor",
    system_message=system_message,
    llm_config={"config_list": [config_list[0]]}
)
