from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, json, dotenv, uuid
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from repositories.message import MessageRepository
from models.message import CreateMessagePayload
from services.chat_search import ChatSearchService
from services.message import MessageService
from datetime import datetime

dotenv.load_dotenv()

router = APIRouter(prefix="/chat-bot", tags=["Chat Bot"])

config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_tour_by_destination",
            "description": "Sử dụng hàm này để tìm kiếm tour du lịch dựa vào một địa điểm hoặc tên tour, trả về tối đa 5 kết quả.",
            "parameters": { 
                "type": "object", 
                "properties": { 
                    "destination_text": { 
                        "type": "string", 
                        "description": "Tên địa điểm người dùng muốn tìm. Ví dụ: 'Đà Nẵng', 'Tour Singapore 3 ngày 2 đêm'"
                    }
                },
                "required": ["destination_text"],
            },
        },
    },
]

class ChatbotRequest(BaseModel):
    chat_id: uuid.UUID
    message: str

@router.post("/")
def chatbot_reply(request: ChatbotRequest):
    user_message_content = request.message.strip()
    
    # === LẤY LỊCH SỬ CHAT GẦN NHẤT ===
    def get_recent_chat_history(chat_id: uuid.UUID, limit: int = 6) -> list:
        """Lấy 6 tin nhắn gần nhất để làm context cho agent"""
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
    
    # Lấy lịch sử chat
    chat_history = get_recent_chat_history(request.chat_id, 6)
    
    # === THIẾT LẬP CÁC AGENT THÔNG MINH ===

    # Agent thực thi
    user_proxy = UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        is_termination_msg=lambda x: "FINAL_ANSWER:" in x.get("content", ""),
        code_execution_config=False,
        system_message="Bạn chỉ thực thi function calls khi được yêu cầu và truyền kết quả cho agent tiếp theo."
    )
    
    # Tạo context message từ lịch sử chat
    context_message = ""
    if chat_history:
        context_message = "\n\n=== LỊCH SỬ CUỘC TRÒ CHUYỆN GẦN ĐÂY ===\n"
        for msg in chat_history:
            role = "Người dùng" if msg["role"] == "user" else "Tôi"
            context_message += f"{role}: {msg['content']}\n"
        context_message += "=== KẾT THÚC LỊCH SỬ ===\n\n"

    # Agent phân tích và tìm kiếm thông minh
    intelligent_coordinator = AssistantAgent(
            name="IntelligentCoordinator",
            system_message=f"""Bạn là trợ lý điều phối thông minh. NHIỆM VỤ CỦA BẠN LÀ PHÂN TÍCH VÀ QUYẾT ĐỊNH HÀNH ĐỘNG, KHÔNG PHẢI LÀ NGƯỜI TRẢ LỜI CUỐI CÙNG (trừ khi chào hỏi).

{context_message}
**QUAN TRỌNG: Dựa vào lịch sử cuộc trò chuyện ở trên để hiểu ngữ cảnh!**

Hãy phân tích tin nhắn người dùng và xử lý theo các tình huống:

**TÌNH HUỐNG 1: Chào hỏi đơn thuần (không có context trước đó)**
- Nếu người dùng chỉ chào hỏi (ví dụ: "Chào", "Hi"):
- Chào lại thân thiện và hỏi họ muốn đi đâu.
- Luôn kết thúc phản hồi bằng dòng: "FINAL_ANSWER": <câu trả lời đầy đủ cho người dùng>
- KHÔNG gọi tool search.

**TÌNH HUỐNG 2: Yêu cầu tìm tour cụ thể**
- Nếu người dùng đề cập địa điểm cụ thể (ví dụ: "tìm tour Đà Nẵng"):
- Gọi function search_tour_by_destination.
- **Sau khi có kết quả, hãy chuyển toàn bộ kết quả cho RecommendationAgent.**
- KHÔNG được dùng FINAL_ANSWER.

**TÌNH HUỐNG 3: Câu hỏi chi tiết/Câu hỏi tiếp theo (CÓ CONTEXT)**
- Nếu người dùng hỏi chi tiết (ví dụ: "giá bao nhiêu", "khởi hành ở đâu", "lịch trình", "có tour X không") VÀ lịch sử chat đã có thông tin:
- **Nhiệm vụ của bạn là chuyển tiếp (forward) câu hỏi này và LỊCH SỬ GẦN NHẤT cho RecommendationAgent để trả lời.**
- (Ví dụ: "RecommendationAgent, người dùng đang hỏi về địa điểm khởi hành của tour chúng ta vừa nói. Hãy trả lời họ.")
- KHÔNG được dùng FINAL_ANSWER.

**Tóm lại: Bạn chỉ được dùng FINAL_ANSWER cho TÌNH HUỐNG 1. Mọi thứ khác liên quan đến tour (tìm kiếm, hỏi chi tiết) đều phải được chuyển cho RecommendationAgent.**
""",
        llm_config={"config_list": config_list, "tools": tools_schema},
    )

    # Agent chuyên gia khuyến nghị
    recommendation_expert = AssistantAgent(
        name="RecommendationAgent", 
        system_message="""Bạn là chuyên gia tư vấn du lịch hàng đầu, có khả năng phân tích sâu sắc để tìm ra lựa chọn hoàn hảo cho khách hàng.

**NHIỆM VỤ:**
Nhiệm vụ của bạn là nhận một danh sách gồm tối đa 3 tour và yêu cầu ban đầu của người dùng. Bạn phải phân tích kỹ lưỡng để chọn ra MỘT tour DUY NHẤT tốt nhất và giải thích lý do một cách thuyết phục.

**QUY TRÌNH SUY LUẬN BẮT BUỘC:**
1.  **Phân tích yêu cầu người dùng:** Đọc lại thật kỹ yêu cầu của người dùng. Họ đang tìm kiếm điều gì? (ví dụ: giá rẻ, nghỉ dưỡng, khám phá, đi với gia đình, ít ngày,...). Ghi nhận những tiêu chí quan trọng nhất.
2.  **So sánh các lựa chọn:** Đối chiếu danh sách tour nhận được với các tiêu chí của người dùng. Tour nào đáp ứng tốt nhất? Tour nào có ưu/nhược điểm gì so với các tour còn lại?
3.  **Đưa ra lựa chọn và lý do:** Chọn ra 1 tour TỐT NHẤT. Phần quan trọng nhất là bạn phải **giải thích được TẠI SAO bạn chọn tour này mà KHÔNG PHẢI các tour kia**. Ví dụ: "Mặc dù tour X có giá rẻ hơn, nhưng tôi đề xuất tour Y vì lịch trình thoải mái, phù hợp hơn với nhu cầu nghỉ dưỡng của bạn."

**FORMAT TRẢ LỜI:**
-   Giới thiệu tour được chọn (tên, giá, thời gian).
-   **Lý do lựa chọn (Quan trọng nhất):** Giải thích rõ ràng tại sao tour này là phương án tối ưu nhất dựa trên phân tích ở trên.
-   Mô tả ngắn gọn lịch trình.
-   Lời khuyên/gợi ý thêm.

**Luôn kết thúc phản hồi bằng dòng: "FINAL_ANSWER": <câu trả lời đầy đủ cho người dùng>**
**LƯU Ý:** Bạn KHÔNG được sử dụng tools, chỉ phân tích dữ liệu nhận được.""",
        llm_config={"config_list": config_list},  # Không có tools
    )

    # === ĐĂNG KÝ FUNCTION VÀ THIẾT LẬP GROUPCHAT ===
    
    user_proxy.register_function(
        function_map={
            "search_tour_by_destination": ChatSearchService.search_tour_by_destination
        }
    )

    # Tạo GroupChat với lịch sử
    groupchat = GroupChat(
        agents=[user_proxy, intelligent_coordinator, recommendation_expert], 
        messages=chat_history,  # Load lịch sử vào GroupChat
        max_round=8,
        speaker_selection_method="auto",
    )
    
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config={"config_list": config_list},
        is_termination_msg=lambda x: "FINAL_ANSWER:" in x.get("content", ""),
    )

    # === BẮT ĐẦU CUỘC TRÒ CHUYỆN ===
    
    try:
        user_proxy.initiate_chat(
            manager,
            message=user_message_content,
        )
        
        # Trích xuất kết quả cuối cùng
        final_answer = "Xin lỗi, đã có lỗi xảy ra trong quá trình xử lý."
        tour_detail = None

        # Tìm FINAL_ANSWER từ bất kỳ agent nào
        chat_messages = groupchat.messages
        for msg in reversed(chat_messages):
            content = msg.get("content", "")
            if "FINAL_ANSWER:" in content:
                final_answer = content.split("FINAL_ANSWER:")[1].strip()
                break
                
        # Tìm kết quả tool call để trả về tour_detail
        for msg in reversed(chat_messages):
            if msg.get("role") == "tool":
                try:
                    tool_content = json.loads(msg.get("content", "{}"))
                    if "tours" in tool_content:
                        tour_detail = tool_content["tours"]
                        break
                except (json.JSONDecodeError, Exception):
                    continue

        # Lưu tin nhắn vào database
        MessageService.create_message(CreateMessagePayload(
            chat_id=request.chat_id, 
            content=user_message_content, 
            role="user"
        ))
        MessageService.create_message(CreateMessagePayload(
            chat_id=request.chat_id, 
            content=final_answer, 
            role="assistant"
        ))

        return {
            # "status": "success",
            "reply": final_answer,
            # "tour_detail": tour_detail 
        }
        
    except Exception as e:
        print(f"⚠️ Lỗi trong quá trình xử lý: {str(e)}")
        error_message = "Xin lỗi, hệ thống đang gặp sự cố. Vui lòng thử lại sau."
        
        try:
            MessageService.create_message(CreateMessagePayload(
                chat_id=request.chat_id, 
                content=user_message_content, 
                role="user"
            ))
            MessageService.create_message(CreateMessagePayload(
                chat_id=request.chat_id, 
                content=error_message, 
                role="assistant"
            ))
        except Exception as db_error:
            print(f"⚠️ Lỗi lưu tin nhắn: {str(db_error)}")
            
        return {
            "status": "error",
            "reply": error_message,
            # "tour_detail": None
        }