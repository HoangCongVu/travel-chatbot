"""
Service xử lý business logic cho chatbot
"""
import json
import uuid
from autogen import GroupChat, GroupChatManager
from services.message import MessageService
from models.message import CreateMessagePayload
from utils.chat_history import get_recent_chat_history, format_context_message
from agents.chatbot_agents import (
    CONFIG_LIST,
    create_user_proxy_agent,
    create_coordinator_agent,
    create_recommendation_agent
)


class ChatbotService:
    """Service xử lý chatbot business logic"""
    
    @staticmethod
    def _extract_final_answer(chat_messages: list) -> str:
        """
        Trích xuất FINAL_ANSWER từ messages
        
        Args:
            chat_messages: List các messages từ groupchat
            
        Returns:
            Final answer string
        """
        for msg in reversed(chat_messages):
            content = msg.get("content", "")
            if "FINAL_ANSWER:" in content:
                return content.split("FINAL_ANSWER:")[1].strip()
        
        return "Xin lỗi, đã có lỗi xảy ra trong quá trình xử lý."
    
    @staticmethod
    def _extract_tour_detail(chat_messages: list):
        """
        Trích xuất tour detail từ tool call results
        
        Args:
            chat_messages: List các messages từ groupchat
            
        Returns:
            Tour detail hoặc None
        """
        for msg in reversed(chat_messages):
            if msg.get("role") == "tool":
                try:
                    tool_content = json.loads(msg.get("content", "{}"))
                    if "tours" in tool_content:
                        return tool_content["tours"]
                except (json.JSONDecodeError, Exception):
                    continue
        return None
    
    @staticmethod
    def process_chat(chat_id: uuid.UUID, user_message: str) -> dict:
        """
        Xử lý tin nhắn chat từ user
        
        Args:
            chat_id: ID cuộc trò chuyện
            user_message: Nội dung tin nhắn từ user
            
        Returns:
            Dict chứa reply
        """
        try:
            # ✅ VALIDATION: Kiểm tra tin nhắn hợp lệ
            if not user_message or not user_message.strip():
                return {
                    "reply": "Xin lỗi, tôi chưa nhận được tin nhắn từ bạn. Bạn muốn hỏi gì ạ? 😊"
                }
            
            # Loại bỏ khoảng trắng thừa
            user_message = user_message.strip()
            
            # Lấy lịch sử chat
            chat_history = get_recent_chat_history(chat_id, 6)
            context_message = format_context_message(chat_history)
            
            # Tạo agents
            user_proxy = create_user_proxy_agent()
            intelligent_coordinator = create_coordinator_agent(context_message)
            recommendation_expert = create_recommendation_agent()
            
            # Tạo GroupChat
            groupchat = GroupChat(
                agents=[user_proxy, intelligent_coordinator, recommendation_expert], 
                messages=chat_history,
                max_round=15,
                speaker_selection_method="auto",
                allow_repeat_speaker=False,  # Không cho phép cùng một speaker nói liên tục
            )
            
            manager = GroupChatManager(
                groupchat=groupchat,
                llm_config={"config_list": CONFIG_LIST},
                is_termination_msg=lambda x: x.get("content") is not None and "FINAL_ANSWER:" in x.get("content", ""),
            )
            
            # Bắt đầu chat
            user_proxy.initiate_chat(manager, message=user_message)
            
            # Trích xuất kết quả
            final_answer = ChatbotService._extract_final_answer(groupchat.messages)
            tour_detail = ChatbotService._extract_tour_detail(groupchat.messages)
            
            # Lưu tin nhắn vào database
            MessageService.create_message(CreateMessagePayload(
                chat_id=chat_id, 
                content=user_message, 
                role="user"
            ))
            MessageService.create_message(CreateMessagePayload(
                chat_id=chat_id, 
                content=final_answer, 
                role="assistant"
            ))
            
            return {
                "reply": final_answer,
            }
            
        except Exception as e:
            print(f"⚠️ Lỗi trong quá trình xử lý: {str(e)}")
            error_message = "Xin lỗi, hệ thống đang gặp sự cố. Vui lòng thử lại sau."
            
            try:
                MessageService.create_message(CreateMessagePayload(
                    chat_id=chat_id, 
                    content=user_message, 
                    role="user"
                ))
                MessageService.create_message(CreateMessagePayload(
                    chat_id=chat_id, 
                    content=error_message, 
                    role="assistant"
                ))
            except Exception as db_error:
                print(f"⚠️ Lỗi lưu tin nhắn: {str(db_error)}")
            
            return {
                "status": "error",
                "reply": error_message,
            }
