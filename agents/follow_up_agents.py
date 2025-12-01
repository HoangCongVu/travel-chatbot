"""
Cấu hình cho tính năng Follow-up (Đeo bám user)
Đọc từ database, fallback về default nếu DB chưa có
"""
import random
from repositories.follow_up_settings import FollowUpSettingsRepository


class FollowUpConfig:
    """Cấu hình follow-up - ĐỌC TỪ DATABASE"""
    
    # ===== KHO TEMPLATE CHO KHÁCH VÃNG LAI (Static) =====
    GENERIC_TEMPLATES = [
        "Alo bạn ơi, bạn còn đó không? Travel AI vẫn đang chờ hỗ trợ bạn nè! 👋",
        "Hình như bạn đang bận? Khi nào rảnh cứ nhắn tin lại cho mình nhé! 😊",
        "Bạn cần tìm ý tưởng du lịch cho cuối tuần này không? 📅",
        "Đừng ngại hỏi nếu bạn cần thêm thông tin gì nhé! Mình ở đây để giúp bạn. 🙋‍♂️",
        "Có vẻ bạn đã bận rồi nhỉ? Mình vẫn sẵn sàng tư vấn khi bạn quay lại nha! 💬",
        "Bạn có muốn mình gợi ý thêm tour nào không? 🌏",
    ]
    
    # ===== CẤU HÌNH AI (Static) =====
    AI_MODEL = "gpt-4o-mini"
    AI_TEMPERATURE = 0.7
    AI_MAX_TOKENS = 60
    
    AI_SYSTEM_PROMPT = """Bạn là Sales du lịch chuyên nghiệp và thân thiện. User đã xem thông tin tour nhưng chưa phản hồi.

Nhiệm vụ: Tạo 1 câu follow-up ngắn gọn (dưới 25 từ) để tái kích hoạt hội thoại.

Yêu cầu:
- Nếu bot đã gửi nhiều tour: Hỏi user thích tour nào, hoặc cần tư vấn thêm không
- Nếu có thông tin giá cụ thể: Nhấn mạnh giá trị hoặc ưu đãi
- Nếu không tìm thấy tour: Gợi ý mở rộng tiêu chí tìm kiếm
- Nếu biết điểm đến: Đề cập tên địa danh cụ thể để tạo cảm xúc

Tone: Vui vẻ, tự nhiên, không áp lực. Kèm 1 emoji phù hợp.

Ví dụ tốt:
- "Bạn thấy tour Đà Lạt 4 ngày nào phù hợp nhất ạ? 🌸"
- "Có cần mình tư vấn thêm về giá tour không bạn? 😊"
- "Mình có thể tìm tour khác với ngân sách linh hoạt hơn nha! 🌏"

Tránh:
- Câu chung chung kiểu "Bạn còn đó không?"
- Quá dài dòng hoặc nhiều câu hỏi"""
    
    # ===== ĐIỀU KIỆN HIGH INTENT (Static) =====
    # Keys trong meta_data để xác định user có intent cao
    HIGH_INTENT_KEYS = [
        'search_criteria',  # User đã search tour (có destination, min_price, max_price, target_date)
        'tours',            # Bot đã gửi danh sách tour
        'total_found'       # Số lượng tour tìm thấy
    ]
    
    @staticmethod
    def get_settings():
        """Lấy settings từ DB, tạo default nếu chưa có"""
        settings = FollowUpSettingsRepository.get_settings()
        if not settings:
            settings = FollowUpSettingsRepository.create_default_settings()
        return settings
    
    @staticmethod
    def get_random_template() -> str:
        """Lấy ngẫu nhiên 1 template"""
        return random.choice(FollowUpConfig.GENERIC_TEMPLATES)
