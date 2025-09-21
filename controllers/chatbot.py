from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, json, dotenv, uuid
from autogen import AssistantAgent
from repositories.message import MessageRepository
from models.message import CreateMessagePayload
from services.tour import TourService
from services.tour_destination import TourDestinationService
from datetime import datetime
from db import Session

dotenv.load_dotenv()

router = APIRouter(prefix="/chat-bot", tags=["Chat Bot"])

# Config cho LLM
config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

# Schema ép model phải trả lời đúng format
function_schema = {
    "name": "chatbot_reply",
    "description": "Trả lời câu hỏi của người dùng về tour",
    "parameters": {
        "type": "object",
        "properties": {
            "response": {"type": "string"}
        },
        "required": ["response"],
    },
}

# Chatbot Agent
agent = AssistantAgent(
    name="TourAssistant",
    system_message="""
Bạn là trợ lý AI chuyên tư vấn tour du lịch.
Bạn nhận được câu hỏi từ người dùng và thông tin từ database.
- Nếu không liên quan du lịch: trả lời lịch sự, ngắn gọn.
- Nếu liên quan: trả lời dựa trên thông tin có.
- Nếu không tìm thấy thông tin: nói rằng không có dữ liệu.
- Nếu người dùng hỏi về tour nhưng không khớp chính xác, hãy trả lời bằng tour gần nhất trong thông tin cung cấp.
Không được trả lời "không có dữ liệu" nếu trong context có ít nhất một tour.
Trả lời ngắn gọn, tiếng Việt.
""",
    llm_config={
        "config_list": config_list,
        "functions": [function_schema],
    },
)

# Request model
class ChatbotRequest(BaseModel):
    chat_id: uuid.UUID
    message: str


@router.post("/")
def chatbot_reply(request: ChatbotRequest):
    user_message = {"role": "user", "content": request.message}

    tour_detail = None
    answer = "Xin lỗi, tôi chưa rõ ý bạn."

    try:
        # 1️⃣ Xác định intent: ngày hay điểm đến
        target_date = None
        for fmt in ("%d/%m/%Y", "%d/%m"):
            try:
                parsed_date = datetime.strptime(request.message, fmt).date()
                if fmt == "%d/%m":
                    parsed_date = parsed_date.replace(year=datetime.now().year)
                target_date = parsed_date
                break
            except ValueError:
                continue

        if target_date:
            # Người dùng hỏi theo ngày
            tour_results = TourService.tour_by_date(target_date)
            if tour_results:
                # tour_results có thể là list → chỉ lấy name hoặc info cơ bản
                tour_detail = [
                    {"tour_name": t.tour_name} for t in tour_results
                ]
                answer = f"Tôi tìm thấy {len(tour_results)} tour khởi hành vào ngày {target_date.strftime('%d/%m/%Y')}."
            else:
                answer = f"Hiện chưa có tour nào khởi hành vào ngày {target_date.strftime('%d/%m/%Y')}."
        else:
            tour_detail = None  # reset trước khi check
            # Người dùng hỏi theo điểm đến
            destination_results = TourDestinationService.search_by_text(request.message, limit=3)
            if destination_results:
                # Lấy tour_id từ destination đầu tiên
                tour_id = destination_results[0].tour_id
                # Lấy chi tiết tour từ TourService
                tour_obj = TourService.get(tour_id)
                if tour_obj:
                    # ⚠️ bỏ id, chỉ lấy thông tin cần cho user
                    tour_detail = {
                        "tour_name": tour_obj.tour_name,
                    }
                    answer = f"Tôi tìm thấy tour: {tour_obj.tour_name}"
                else:
                    tour_detail = None
                    answer = "Xin lỗi, tôi không tìm thấy chi tiết tour."
            else:
                tour_detail = None
                answer = "Xin lỗi, tôi không tìm thấy tour nào phù hợp."
    except Exception as e:
        print(f"⚠️ Intent detect error: {str(e)}")

    # 2️⃣ Lấy lịch sử chat
    try:
        chat_history_objs = MessageRepository.get_recent_messages(
            chat_id=request.chat_id, limit=10
        )
        # Chuyển sang dạng dict để agent hiểu
        chat_history = [{"role": msg.role, "content": msg.content} for msg in chat_history_objs]
    except Exception as e:
        print(f"⚠️ Lỗi lấy chat history: {str(e)}")
        chat_history = []

    # 3️⃣ Ghép context cho agent
    messages_to_agent = []
    if tour_detail:
        messages_to_agent.append(
            {
                "role": "system",
                "content": f"Thông tin tour: {json.dumps(tour_detail, ensure_ascii=False)}"
            }
        )
    messages_to_agent.extend(chat_history)
    messages_to_agent.append(user_message)

    # 4️⃣ Gọi agent để refine câu trả lời
    try:
        result = agent.generate_reply(messages=messages_to_agent)
        if isinstance(result, dict) and result.get("function_call"):
            args = result["function_call"].get("arguments")
            if args:
                try:
                    response_json = json.loads(args)
                    answer = response_json.get("response", answer)
                except Exception as e:
                    print(f"⚠️ Parse JSON fail: {str(e)}")
        else:
            answer = str(result)
    except Exception as e:
        print(f"⚠️ Lỗi gọi agent: {str(e)}")

    # 5️⃣ Fallback: nếu agent trả lời "không có dữ liệu" nhưng thực tế có tour
    if tour_detail and "không có dữ liệu" in answer.lower():
        if isinstance(tour_detail, list) and len(tour_detail) > 0:
            answer = f"Tôi tìm thấy tour: {tour_detail[0].get('tour_name')}"
        elif isinstance(tour_detail, dict):
            answer = f"Tôi tìm thấy tour: {tour_detail.get('tour_name')}"

    # 6️⃣ Lưu message user
    try:
        MessageRepository.create(
            CreateMessagePayload(
                chat_id=request.chat_id, content=request.message, role="user"
            )
        )
    except Exception as e:
        print(f"⚠️ Lỗi lưu tin nhắn user: {str(e)}")

    # 7️⃣ Lưu message assistant
    try:
        MessageRepository.create(
            CreateMessagePayload(
                chat_id=request.chat_id, content=answer, role="assistant"
            )
        )
    except Exception as e:
        print(f"⚠️ Lỗi lưu tin nhắn assistant: {str(e)}")

    # 8️⃣ Trả về kết quả
    return {
        "status": "success",
        "reply": answer,
        "tour_detail": tour_detail
    }
