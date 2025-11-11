import uuid
from services.message import MessageService


def get_recent_chat_history(chat_id: uuid.UUID, limit: int = 6) -> list:
    """
    Lấy tin nhắn gần nhất để làm context cho agent
    
    Args:
        chat_id: ID của cuộc trò chuyện
        limit: Số lượng tin nhắn tối đa (mặc định 6)
        
    Returns:
        List các message dict với format phù hợp cho autogen
    """
    try:
        recent_messages = MessageService.get_recent_messages(chat_id, limit)
        
        chat_history = []
        for msg in reversed(recent_messages):  # Sắp xếp theo thời gian từ cũ đến mới
            if msg.role == "user":
                chat_history.append({
                    "role": "user", 
                    "content": msg.content,
                    "name": "User"
                })
            else:
                chat_history.append({
                    "role": "assistant", 
                    "content": msg.content,
                    "name": "IntelligentCoordinator"
                })
        
        return chat_history
    except Exception as e:
        print(f"⚠️ Lỗi lấy lịch sử chat: {str(e)}")
        return []


def format_context_message(chat_history: list) -> str:
    """
    Format lịch sử chat thành context message cho agent
    
    Args:
        chat_history: List các message từ get_recent_chat_history
        
    Returns:
        String context message đã được format
    """
    if not chat_history:
        return ""
    
    context_message = "\n\n=== LỊCH SỬ CUỘC TRÒ CHUYỆN GẦN ĐÂY ===\n"
    for msg in chat_history:
        role = "Người dùng" if msg["role"] == "user" else "Tôi"
        context_message += f"{role}: {msg['content']}\n"
    context_message += "=== KẾT THÚC LỊCH SỬ ===\n\n"
    
    return context_message
