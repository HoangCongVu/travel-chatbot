"""
Service xử lý Follow-up Messages (Đeo bám user)
Chiến thuật Hybrid: High Intent -> AI, Low Intent -> Template
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import uuid
from openai import OpenAI
import asyncio

from db import Session
from models.message import Message, CreateMessagePayload
from models.chat import Chat
from models.follow_up_settings import FollowUpSettingsResponse, UpdateFollowUpSettingsRequest
from repositories.message import MessageRepository
from repositories.chat import ChatRepository
from repositories.follow_up_settings import FollowUpSettingsRepository
from agents.follow_up_agents import FollowUpConfig
from utils.facebook_messenger import send_facebook_message
from env import env

# Global OpenAI client
openai_client = OpenAI(api_key=env.OPENAI_API_KEY)


class FollowUpService:
    """Service xử lý logic follow-up messages và settings"""
    @staticmethod
    def get_settings() -> FollowUpSettingsResponse | None:
        """Lấy cấu hình follow-up"""
        return FollowUpSettingsRepository.get_settings()
    
    @staticmethod
    def update_settings(payload: UpdateFollowUpSettingsRequest, admin_id: uuid.UUID | None = None) -> FollowUpSettingsResponse:
        """Cập nhật cấu hình follow-up"""
        return FollowUpSettingsRepository.update_settings(payload, admin_id)
    
    @staticmethod
    def create_default_settings() -> FollowUpSettingsResponse:
        """Tạo settings mặc định (gọi 1 lần duy nhất khi khởi tạo hệ thống)"""
        return FollowUpSettingsRepository.create_default_settings()
    
    def _generate_smart_followup_content(
        self, 
        last_user_msg: str, 
        last_bot_msg: str, 
        meta_data: Optional[Dict]
    ) -> tuple[str, str]:
        """
        Chiến thuật Hybrid:
        - High Intent -> AI
        - Low Intent -> Template
        
        Args:
            last_user_msg: Tin nhắn cuối từ user
            last_bot_msg: Tin nhắn cuối từ bot
            meta_data: Metadata của tin nhắn bot (chứa thông tin về tour, query, etc.)
            
        Returns:
            Tuple (content, strategy) - content là nội dung tin nhắn, strategy là 'ai_generated' hoặc 'template_fallback'
        """
        
        # 1. KIỂM TRA INTENT
        has_high_intent = False
        if meta_data and isinstance(meta_data, dict):
            # Kiểm tra các key quan trọng
            if any(key in meta_data for key in FollowUpConfig.HIGH_INTENT_KEYS):
                has_high_intent = True
        
        # === TRƯỜNG HỢP 1: KHÁCH TIỀM NĂNG (Dùng AI) ===
        if has_high_intent:
            try:
                print(f"💰 High Intent detected! Calling AI...")
                
                # Xây dựng context string chi tiết
                details = []
                
                # 1. Trích xuất search criteria
                search_criteria = meta_data.get("search_criteria", {})
                if search_criteria:
                    destination = search_criteria.get("destination")
                    min_price = search_criteria.get("min_price")
                    max_price = search_criteria.get("max_price")
                    target_date = search_criteria.get("target_date")
                    
                    if destination:
                        details.append(f"- Điểm đến: {destination}")
                    if min_price or max_price:
                        price_range = []
                        if min_price:
                            price_range.append(f"từ {min_price:,.0f}đ")
                        if max_price:
                            price_range.append(f"đến {max_price:,.0f}đ")
                        details.append(f"- Ngân sách: {' '.join(price_range)}")
                    if target_date:
                        details.append(f"- Ngày muốn đi: {target_date}")
                
                # 2. Trích xuất thông tin tours
                tours = meta_data.get("tours", [])
                total_found = meta_data.get("total_found", 0)
                
                if tours and len(tours) > 0:
                    details.append(f"- Bot đã gửi {total_found} tour cho user xem:")
                    # Liệt kê tối đa 3 tour đầu tiên
                    for i, tour in enumerate(tours[:3], 1):
                        tour_name = tour.get("tour_name", "")
                        days = tour.get("days", "")
                        
                        # Lấy giá từ price_by_packages hoặc price_by_dates
                        price_info = ""
                        price_packages = tour.get("price_by_packages", [])
                        if price_packages and len(price_packages) > 0:
                            price = price_packages[0].get("price", 0)
                            if price > 0:
                                price_info = f" - {price:,.0f}đ"
                        
                        tour_info = f"  {i}. {tour_name}"
                        if days:
                            tour_info += f" ({days} ngày)"
                        if price_info:
                            tour_info += price_info
                        details.append(tour_info)
                    
                    if len(tours) > 3:
                        details.append(f"  ... và {len(tours) - 3} tour khác")
                elif total_found == 0:
                    details.append("- Bot không tìm thấy tour phù hợp")
                
                # 3. Fallback: Check deprecated keys cho tương thích ngược
                if not details:
                    if meta_data.get("destination"): 
                        details.append(f"- Nơi muốn đến: {meta_data['destination']}")
                    if meta_data.get("price_range"): 
                        details.append(f"- Ngân sách: {meta_data['price_range']}")
                    if meta_data.get("dates"): 
                        details.append(f"- Thời gian: {meta_data['dates']}")
                    if meta_data.get("tours"): 
                        details.append("- Bot đã gửi danh sách tour cho user xem.")
                
                context_str = "\n".join(details) if details else "User quan tâm tour nhưng chưa chốt."
                
                # Gọi AI
                response = openai_client.chat.completions.create(
                    model=FollowUpConfig.AI_MODEL,
                    messages=[
                        {"role": "system", "content": FollowUpConfig.AI_SYSTEM_PROMPT},
                        {"role": "user", "content": f"User: {last_user_msg}\nBot: {last_bot_msg}\nContext:\n{context_str}"}
                    ],
                    temperature=FollowUpConfig.AI_TEMPERATURE,
                    max_tokens=FollowUpConfig.AI_MAX_TOKENS
                )
                
                content = response.choices[0].message.content.strip()
                return content, "ai_generated"
                
            except Exception as e:
                print(f"⚠️ AI Error: {e}. Falling back to template.")
                # Rơi xuống logic template
        
        # === TRƯỜNG HỢP 2: FALLBACK / LOW INTENT ===
        print(f"🆓 Using Template strategy.")
        content = FollowUpConfig.get_random_template()
        return content, "template_fallback"
    
    def _get_last_messages(self, chat_id: uuid.UUID) -> tuple[str, str, Optional[Dict]]:
        """
        Lấy 2 tin nhắn cuối cùng (bot và user) từ database
        
        Args:
            chat_id: ID của chat
            
        Returns:
            Tuple (last_user_msg, last_bot_msg, last_bot_meta)
        """
        with Session() as session:
            # Lấy 2 tin nhắn cuối
            messages = (
                session.query(Message)
                .filter(Message.chat_id == chat_id)
                .order_by(Message.created_at.desc())
                .limit(2)
                .all()
            )
            
            if not messages:
                return "(Bắt đầu chat)", "", None
            
            # Tin nhắn đầu tiên là tin nhắn mới nhất (bot)
            last_bot_msg = messages[0].content if messages else ""
            last_bot_meta = messages[0].meta_data if messages else None
            
            # Tin nhắn thứ 2 là tin nhắn từ user
            last_user_msg = messages[1].content if len(messages) > 1 else "(Bắt đầu chat)"
            
            return last_user_msg, last_bot_msg, last_bot_meta
    
    def send_follow_up_message(self, chat_id: uuid.UUID) -> Optional[uuid.UUID]:
        """
        Gửi tin nhắn follow-up cho 1 chat
        
        Args:
            chat_id: ID của chat cần follow-up
            
        Returns:
            ID của message mới tạo hoặc None nếu có lỗi
        """
        try:
            # 0. Lấy thông tin chat để biết platform
            chat = ChatRepository.get_one(chat_id)
            
            # 1. Lấy tin nhắn cũ để tạo context
            last_user_msg, last_bot_msg, last_bot_meta = self._get_last_messages(chat_id)
            
            # 2. Sinh nội dung follow-up
            content, strategy = self._generate_smart_followup_content(
                last_user_msg, 
                last_bot_msg, 
                last_bot_meta
            )
            
            # 3. Tạo message mới
            message_payload = CreateMessagePayload(
                chat_id=chat_id,
                role="assistant",
                content=content,
                meta_data={
                    "is_follow_up": True
                }
            )
            
            # 4. Lưu vào database
            new_message = MessageRepository.create(message_payload)
            
            # 5. Gửi lên platform tương ứng (Facebook, Zalo, etc.)
            if chat.platform == "facebook" and chat.external_user_id:
                try:
                    # Gửi lên Facebook Messenger
                    result = asyncio.run(send_facebook_message(chat.external_user_id, content))
                    
                    if result.get("status") == "success":
                        print(f"✅ Sent follow-up [{strategy}] to Facebook user {chat.external_user_id}: {content[:50]}...")
                    else:
                        print(f"⚠️ Failed to send to Facebook: {result.get('error')}")
                        
                except Exception as fb_error:
                    print(f"❌ Error sending to Facebook: {fb_error}")
            elif chat.platform is None and chat.user_id:
                # Web chat của user đã đăng ký - chỉ lưu DB
                print(f"✅ Sent follow-up [{strategy}] for web user {chat.user_id} (DB only): {content[:50]}...")
            else:
                # Trường hợp khác (khách vãng lai) - không nên xảy ra vì đã filter trong query
                print(f"⚠️ Skipped follow-up for chat {chat_id} (guest user)")
            
            return new_message.id
            
        except Exception as e:
            print(f"❌ Error sending follow-up for chat {chat_id}: {e}")
            return None
    
    def get_chats_need_followup(self) -> List[uuid.UUID]:
        """
        Tìm các chat cần gửi follow-up
        
        Logic:
        - Tính năng phải BẬT (DB: is_enabled=True)
        - Tin nhắn cuối là từ bot (role='assistant')
        - Đã qua thời gian chờ
        - Chưa gửi quá max_count lần
        - Trong khung giờ hoạt động
        
        Returns:
            List các chat_id cần follow-up
        """
        # Lấy cấu hình từ DB
        settings = FollowUpConfig.get_settings()
        
        # Kiểm tra tính năng có bật không
        if not settings.is_enabled:
            print(f"⏸️ Follow-up feature is DISABLED. Skipping scan.")
            return []
        
        with Session() as session:
            now = datetime.now()
            
            # 1. Kiểm tra khung giờ hoạt động
            current_hour = now.hour
            if not (settings.active_hours_start <= current_hour < settings.active_hours_end):
                print(f"⏰ Outside active hours ({current_hour}h). Skipping follow-up scan.")
                return []
            
            # 2. Tính thời điểm cần follow-up
            follow_up_threshold = now - timedelta(minutes=settings.delay_minutes)
            
            # 3. Query: Lấy các chat có tin nhắn cuối từ bot (KHÔNG PHẢI follow-up) và đã qua thời gian chờ
            # Subquery: Lấy tin nhắn bot THẬT (không phải follow-up) mới nhất của mỗi chat
            from sqlalchemy import func, and_
            from sqlalchemy import or_
            
            # Subquery để lấy tin nhắn bot THẬT mới nhất của mỗi chat
            subquery = (
                session.query(
                    Message.chat_id,
                    func.max(Message.created_at).label('last_real_bot_message_time')
                )
                .filter(
                    Message.role == "assistant",
                    # Chỉ lấy tin nhắn bot THẬT (không phải follow-up)
                    or_(
                        Message.meta_data['is_follow_up'].astext.is_(None),
                        Message.meta_data['is_follow_up'].astext != 'true'
                    )
                )
                .group_by(Message.chat_id)
                .subquery()
            )
            
            # Query chính: Join với subquery và Chat table để lọc platform
            last_real_bot_messages = (
                session.query(Message)
                .join(Chat, Message.chat_id == Chat.id)  # Join với Chat table
                .join(
                    subquery,
                    and_(
                        Message.chat_id == subquery.c.chat_id,
                        Message.created_at == subquery.c.last_real_bot_message_time
                    )
                )
                .filter(
                    Message.created_at <= follow_up_threshold,  # Đã qua thời gian chờ
                    # Điều kiện: (platform='facebook' + có external_user_id) HOẶC (platform NULL + có user_id)
                    or_(
                        and_(
                            Chat.platform == "facebook",
                            Chat.external_user_id.isnot(None)
                        ),
                        and_(
                            Chat.platform.is_(None),
                            Chat.user_id.isnot(None)
                        )
                    )
                )
                .all()
            )
            
            # 4. Lọc thêm: Kiểm tra số lần đã follow-up SAU tin nhắn bot THẬT
            result = []
            for msg in last_real_bot_messages:
                # Đếm số follow-up messages đã gửi SAU tin nhắn bot THẬT này
                follow_up_count = (
                    session.query(func.count(Message.id))
                    .filter(
                        Message.chat_id == msg.chat_id,
                        Message.meta_data['is_follow_up'].astext == 'true',
                        Message.created_at > msg.created_at  # Chỉ đếm follow-up SAU tin nhắn bot THẬT
                    )
                    .scalar()
                )
                
                # Nếu chưa đủ số lần follow-up
                if follow_up_count < settings.max_count:
                    result.append(msg.chat_id)
            
            print(f"🔍 Found {len(result)} chats need follow-up (Facebook + Web registered users)")
            return result
    
    def process_all_followups(self) -> Dict[str, int]:
        """
        Xử lý tất cả các chat cần follow-up
        
        Returns:
            Dict chứa thống kê: {'success': X, 'failed': Y, 'total': Z}
        """
        chat_ids = self.get_chats_need_followup()
        
        stats = {
            'success': 0,
            'failed': 0,
            'total': len(chat_ids)
        }
        
        for chat_id in chat_ids:
            result = self.send_follow_up_message(chat_id)
            if result:
                stats['success'] += 1
            else:
                stats['failed'] += 1
        
        print(f"📊 Follow-up stats: {stats}")
        return stats
