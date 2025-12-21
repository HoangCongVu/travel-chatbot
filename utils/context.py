"""
Context management cho chatbot - Thread-safe context variables
"""
from contextvars import ContextVar
from typing import Optional

# Context variables cho chatbot
current_chat_id: ContextVar[Optional[str]] = ContextVar('current_chat_id', default=None)
current_user_id: ContextVar[Optional[str]] = ContextVar('current_user_id', default=None)
current_session_id: ContextVar[Optional[str]] = ContextVar('current_session_id', default=None)


class ChatContext:
    """Helper class để quản lý context"""
    
    @staticmethod
    def set(chat_id: str = None, user_id: str = None, session_id: str = None):
        """
        Set context cho request hiện tại
        
        Args:
            chat_id: UUID của chat
            user_id: UUID của user (nếu đã đăng nhập)
            session_id: UUID của session (nếu khách vãng lai)
        """
        if chat_id:
            current_chat_id.set(chat_id)
        if user_id:
            current_user_id.set(user_id)
        if session_id:
            current_session_id.set(session_id)
    
    @staticmethod
    def get_chat_id() -> Optional[str]:
        """Lấy chat_id từ context"""
        return current_chat_id.get()
    
    @staticmethod
    def get_user_id() -> Optional[str]:
        """Lấy user_id từ context"""
        return current_user_id.get()
    
    @staticmethod
    def get_session_id() -> Optional[str]:
        """Lấy session_id từ context"""
        return current_session_id.get()
    
    @staticmethod
    def get_all() -> dict:
        """Lấy tất cả context"""
        return {
            'chat_id': current_chat_id.get(),
            'user_id': current_user_id.get(),
            'session_id': current_session_id.get()
        }
    
    @staticmethod
    def clear():
        """Xóa context (cleanup sau khi request kết thúc)"""
        current_chat_id.set(None)
        current_user_id.set(None)
        current_session_id.set(None)
