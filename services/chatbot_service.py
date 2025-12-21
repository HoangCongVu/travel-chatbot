"""
Service xử lý business logic cho chatbot
"""
import json
import ast
import uuid
import asyncio
from autogen import GroupChat, GroupChatManager
from services.message import MessageService
from models.message import CreateMessagePayload
from utils.chat_history import get_recent_chat_history, format_context_message
from utils.socket_manager import emit_socket_safely
from agents.chatbot_agents import (
    CONFIG_LIST,
    create_user_proxy_agent,
    create_coordinator_agent,
    create_planner_agent,
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
    def _extract_metadata(chat_messages: list) -> dict:
        """
        Trích xuất metadata từ chat messages để lưu vào database
        CHỈ lưu kết quả từ search_tour_chat (KHÔNG lưu search_web_information)
        
        Args:
            chat_messages: List các messages từ groupchat
            
        Returns:
            Dict chứa metadata (tour results) hoặc None
        """
        for msg in reversed(chat_messages):
            role = msg.get("role", "")
            content = msg.get("content", "")
            
            if role == "tool":
                try:
                    # Parse content
                    if isinstance(content, dict):
                        tool_content = content
                    elif isinstance(content, str):
                        # Content có thể chứa NHIỀU tool responses trên nhiều dòng
                        # Split by blank lines và parse từng phần
                        parts = content.split('\n\n')
                        
                        parsed_results = []
                        for part in parts:
                            part = part.strip()
                            if not part:
                                continue
                            
                            # Thử parse từng part
                            try:
                                parsed_results.append(ast.literal_eval(part))
                                continue
                            except (ValueError, SyntaxError):
                                pass
                            
                            try:
                                parsed_results.append(json.loads(part))
                                continue
                            except json.JSONDecodeError:
                                pass
                            
                            try:
                                parsed_results.append(eval(part))
                            except Exception:
                                pass
                        
                        # Tìm result có "tours" key (và không có "sources")
                        if not parsed_results:
                            continue
                        
                        for result in parsed_results:
                            if isinstance(result, dict):
                                has_tours = "tours" in result
                                has_sources = "sources" in result
                                
                                if has_tours and not has_sources:
                                    tool_content = result
                                    break
                        else:
                            continue
                    else:
                        continue
                    
                    # CHỈ lấy nếu có key "tours" và tours không rỗng
                    # BỎ QUA nếu có "sources" (đó là web search, không phải tour search)
                    has_tours = isinstance(tool_content, dict) and "tours" in tool_content
                    has_sources = isinstance(tool_content, dict) and "sources" in tool_content
                    tours_not_empty = has_tours and bool(tool_content.get("tours"))
                    
                    if has_tours and tours_not_empty and not has_sources:
                        return tool_content
                        
                except Exception:
                    continue
        
        return None
    
    @staticmethod
    def process_chat(chat_id: uuid.UUID, user_message: str, user_id: uuid.UUID = None, session_id: uuid.UUID = None) -> dict:
        """
        Xử lý tin nhắn chat từ user
        
        Args:
            chat_id: ID cuộc trò chuyện
            user_message: Nội dung tin nhắn từ user
            user_id: ID user nếu đã đăng nhập  
            session_id: Session ID nếu khách vãng lai
            
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
            
            # Lấy cả lịch sử chat VÀ tour context trong 1 lần query
            context_data = get_recent_chat_history(chat_id, 10)
            chat_history = context_data["chat_history"]
            tour_context = context_data["tour_context"]
            
            # ⚠️ QUAN TRỌNG: Thêm message hiện tại vào lịch sử
            # Vì message mới vừa được tạo ở controller nhưng chưa xuất hiện trong get_recent_chat_history
            # Cần thêm thủ công để IntelligentCoordinator có thể đọc được
            chat_history_with_current = chat_history + [{"role": "user", "content": user_message}]
            context_message = format_context_message(chat_history_with_current)
            
            # 📊 LOG: Hiển thị lịch sử chat và tour context
            print("\n" + "="*80)
            print("📋 LỊCH SỬ CHAT ĐƯỢC TRUYỀN VÀO AGENT:")
            print("="*80)
            if chat_history:
                for idx, msg in enumerate(chat_history, 1):
                    role_display = "👤 User" if msg["role"] == "user" else "🤖 Assistant"
                    print(f"{idx}. {role_display}: {msg['content'][:100]}...")
            else:
                print("   (Không có lịch sử)")
            
            print("\n" + "="*80)
            print("🎯 TOUR CONTEXT:")
            print("="*80)
            if tour_context:
                import json
                print(json.dumps(tour_context, ensure_ascii=False, indent=2)[:500] + "...")
            else:
                print("   (Không có tour context)")
            print("="*80 + "\n")
            
            # Tạo agents với kiến trúc mới (4 agents)
            user_proxy = create_user_proxy_agent()
            intelligent_coordinator = create_coordinator_agent(context_message)  # Lễ tân - chỉ nhận context_message
            planner_agent = create_planner_agent(context_message, tour_context)  # Nhạc trưởng - nhận cả tour_context
            recommendation_expert = create_recommendation_agent()
            
            # 🔧 INJECT CONTEXT vào agents để hỗ trợ booking
            # Add chat_id, user_id, session_id vào environment cho các tools
            import os
            os.environ['CURRENT_CHAT_ID'] = str(chat_id)
            if user_id:
                os.environ['CURRENT_USER_ID'] = str(user_id)
            else:
                os.environ.pop('CURRENT_USER_ID', None)
            if session_id:
                os.environ['CURRENT_SESSION_ID'] = str(session_id)
            else:
                os.environ.pop('CURRENT_SESSION_ID', None)
            
            # 🔧 Custom speaker selection để LUÔN GỌI IntelligentCoordinator TRƯỚC
            def custom_speaker_selection(last_speaker, groupchat):
                """
                Luồng xử lý:
                1. UserProxy → IntelligentCoordinator (LUÔN LUÔN)
                2. IntelligentCoordinator → PlannerAgent hoặc kết thúc
                3. PlannerAgent → UserProxy (execute tools) 
                4. UserProxy (tool results) → RecommendationAgent
                5. RecommendationAgent → kết thúc
                """
                messages = groupchat.messages
                if not messages:
                    return intelligent_coordinator
                
                last_message = messages[-1] if messages else None
                last_speaker_name = last_speaker.name if last_speaker else None
                
                # 1️⃣ Sau khi UserProxy gửi user message → LUÔN GỌI IntelligentCoordinator
                if last_speaker_name == "UserProxy":
                    # Kiểm tra xem có phải tool result không
                    if last_message and last_message.get("role") == "tool":
                        # ⚠️ QUAN TRỌNG: Kiểm tra xem có phải kết quả từ quick_book_tour không
                        # Nếu đúng → CHUYỂN THẲNG CHO RecommendationAgent (KHÔNG cho PlannerAgent gọi lại)
                        content = last_message.get("content", "")
                        
                        # Parse tool result để kiểm tra
                        is_booking_result = False
                        try:
                            if isinstance(content, dict):
                                is_booking_result = "booking_id" in content.get("data", {})
                            elif isinstance(content, str):
                                is_booking_result = "booking_id" in content
                        except:
                            pass
                        
                        if is_booking_result:
                            # Tool result từ quick_book_tour → CHUYỂN THẲNG RecommendationAgent
                            print("🚨 Phát hiện booking result → BẮT BUỘC chuyển RecommendationAgent")
                            return recommendation_expert
                        else:
                            # Tool result khác (search_tour_chat, search_web_information) → TRẢ VỀ PlannerAgent
                            return planner_agent
                    else:
                        # User message → LUÔN GỌI IntelligentCoordinator
                        return intelligent_coordinator
                
                # 2️⃣ Sau IntelligentCoordinator → PlannerAgent hoặc kết thúc
                elif last_speaker_name == "IntelligentCoordinator":
                    content = last_message.get("content", "") if last_message else ""
                    if "FINAL_ANSWER:" in content:
                        # IntelligentCoordinator đã trả lời → kết thúc
                        return None
                    else:
                        # IntelligentCoordinator chuyển công việc → PlannerAgent
                        return planner_agent
                
                # 3️⃣ Sau PlannerAgent → kiểm tra nội dung
                elif last_speaker_name == "PlannerAgent":
                    content = last_message.get("content", "") if last_message else ""
                    # Nếu PlannerAgent mention RecommendationAgent → chuyển cho RecommendationAgent
                    if "RecommendationAgent" in content:
                        return recommendation_expert
                    # Nếu không → execute tools qua UserProxy
                    else:
                        return user_proxy
                
                # 4️⃣ Sau RecommendationAgent → kết thúc (có FINAL_ANSWER)
                elif last_speaker_name == "RecommendationAgent":
                    return None
                
                # Default: IntelligentCoordinator
                return intelligent_coordinator
            
            # Tạo GroupChat với 4 agents
            groupchat = GroupChat(
                agents=[user_proxy, intelligent_coordinator, planner_agent, recommendation_expert], 
                messages=chat_history,
                max_round=15,
                speaker_selection_method=custom_speaker_selection,
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
            metadata = ChatbotService._extract_metadata(groupchat.messages)
            
            print(f"📊 Metadata extracted: {metadata is not None}")
            if metadata:
                print(f"   - Tours found: {len(metadata.get('tours', []))}")
                print(f"   - Total found: {metadata.get('total_found', 0)}")
            
            # Lưu assistant message với metadata từ tool (nếu có)
            assistant_msg = MessageService.create_message(CreateMessagePayload(
                chat_id=chat_id, 
                content=final_answer, 
                role="assistant",
                meta_data=metadata
            ))
            
            # 🔥 Emit socket event cho assistant message
            emit_socket_safely(str(chat_id), {
                "message_id": str(assistant_msg.id),
                "chat_id": str(chat_id),
                "content": final_answer,
                "role": "assistant",
                "created_at": assistant_msg.created_at.isoformat() if assistant_msg.created_at else None,
                "meta_data": metadata
            })
            
            print(f"💾 Assistant message saved with meta_data: {assistant_msg.meta_data is not None}")
            
            # 🧹 CLEANUP: Xóa environment variables sau khi xử lý
            os.environ.pop('CURRENT_CHAT_ID', None)
            os.environ.pop('CURRENT_USER_ID', None) 
            os.environ.pop('CURRENT_SESSION_ID', None)
            
            return {
                "reply": final_answer,
            }
            
        except Exception as e:
            print(f"⚠️ Lỗi trong quá trình xử lý: {str(e)}")
            error_message = "Xin lỗi, hệ thống đang gặp sự cố. Vui lòng thử lại sau."
            
            try:
                # ⚠️ KHÔNG tạo user message - đã tạo ở chatbot controller
                # Chỉ lưu error message
                error_msg = MessageService.create_message(CreateMessagePayload(
                    chat_id=chat_id, 
                    content=error_message, 
                    role="assistant"
                ))
                
                # 🔥 Emit socket event cho error message
                emit_socket_safely(str(chat_id), {
                    "message_id": str(error_msg.id),
                    "chat_id": str(chat_id),
                    "content": error_message,
                    "role": "assistant",
                    "created_at": error_msg.created_at.isoformat() if error_msg.created_at else None,
                    "meta_data": error_msg.meta_data
                })
                    
            except Exception as db_error:
                print(f"⚠️ Lỗi lưu tin nhắn: {str(db_error)}")
            
            return {
                "status": "error",
                "reply": error_message,
            }
