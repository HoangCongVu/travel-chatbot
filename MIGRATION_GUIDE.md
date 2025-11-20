# Migration Guide: Kiến trúc Modular với PlannerAgent

## 📊 Tổng quan

### Kiến trúc

```
User → IntelligentCoordinator (LỄ TÂN - Phân loại + Route tin nhắn)
                ↓
         PlannerAgent (NHẠC TRƯỞNG - Lập kế hoạch + Gọi tools + Điều phối)
                ↓
         UserProxy (THỰC THI - Execute tools)
                ↓
         RecommendationAgent (TƯ VẤN - Trình bày chuyên nghiệp)
```

**Ưu điểm:**

- Mỗi agent có trách nhiệm rõ ràng
- System message ngắn gọn, dễ hiểu
- Dễ debug: Biết lỗi ở agent nào
- Dễ mở rộng: Thêm agent mới không ảnh hưởng cũ

---

## 🔄 So sánh chi tiết

| Tiêu chí                   | Kiến trúc CŨ                               | Kiến trúc MỚI                                 |
| -------------------------- | ------------------------------------------ | --------------------------------------------- |
| **Số lượng agents**        | 3 agents                                   | 4 agents                                      |
| **IntelligentCoordinator** | Phân tích + Gọi tool + Điều phối + Trả lời | Chỉ phân loại + route (như lễ tân)            |
| **PlannerAgent**           | ❌ Không có                                | ✅ Lập kế hoạch + Gọi tools + Điều phối       |
| **System message length**  | ~800 dòng (Coordinator)                    | ~150 dòng (Coordinator) + ~250 dòng (Planner) |
| **Độ phức tạp logic**      | Tất cả tập trung ở Coordinator             | Phân tán rõ ràng                              |
| **Khả năng debug**         | Khó (nhiều logic lẫn lộn)                  | Dễ (mỗi agent 1 nhiệm vụ)                     |
| **Khả năng mở rộng**       | Khó (phải sửa Coordinator)                 | Dễ (thêm module mới)                          |

---

## 📋 Luồng xử lý chi tiết

### Ví dụ 1: User chào hỏi "Xin chào"

**Kiến trúc MỚI:**

```
User: "Xin chào"
  ↓
Coordinator (Lễ tân): Phân tích → Nhận diện chào hỏi → Tự trả lời FINAL_ANSWER
  (KHÔNG chuyển PlannerAgent vì là tin nhắn đơn giản)
```

✅ **Kết quả:** Giống nhau, nhưng logic ngắn gọn hơn

---

### Ví dụ 2: User tìm tour "Tìm tour Đà Nẵng giá rẻ"

**Kiến trúc MỚI:**

```
User: "Tìm tour Đà Nẵng giá rẻ"
  ↓
Coordinator (Lễ tân):
  - Nhận diện: Yêu cầu tìm tour (phức tạp)
  - Chuyển ngay: "PlannerAgent, người dùng muốn tìm tour Đà Nẵng giá rẻ"
  ↓
PlannerAgent (Nhạc trưởng):
  - Phân tích: Cần tìm tour
  - Trích xuất: destination="Đà Nẵng", max_price=??? (không xác định → không set)
  - Lập kế hoạch: Gọi search_tour_chat
  - Gọi tool
  - Nhận kết quả
  - Quyết định: Có tour → "RecommendationAgent, user muốn xem nhiều lựa chọn. Data: [...]"
  ↓
UserProxy: Thực thi search_tour_chat
  ↓
RecommendationAgent: Trình bày FINAL_ANSWER
```

✅ **Lợi ích:**

- Coordinator nhẹ hơn (chỉ route)
- PlannerAgent tập trung xử lý logic phức tạp
- Dễ debug: Biết lỗi ở PlannerAgent hay RecommendationAgent

---

### Ví dụ 3: User hỏi "Hà Nội có gì vui?"

**Kiến trúc MỚI:**

```
User: "Hà Nội có gì vui?"
  ↓
Coordinator (Lễ tân):
  - Nhận diện: Câu hỏi về địa điểm (phức tạp)
  - Chuyển: "PlannerAgent, người dùng hỏi: Hà Nội có gì vui?"
  ↓
PlannerAgent (Nhạc trưởng):
  - Phân tích: Cần thông tin web
  - Lập kế hoạch: Gọi search_web_information
  - Gọi tool("Hà Nội có gì vui")
  - Nhận kết quả
  - Chuyển: "RecommendationAgent, user hỏi về Hà Nội. Data: [...]"
  ↓
UserProxy: Thực thi search_web_information
  ↓
RecommendationAgent: Tổng hợp 3-5 điểm nổi bật + FINAL_ANSWER
```

✅ **Lợi ích:** Tách biệt rõ routing (Coordinator) vs planning (PlannerAgent)

---
