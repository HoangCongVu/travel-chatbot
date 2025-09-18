from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, json, dotenv
from autogen import AssistantAgent
import uuid
from repositories.message import MessageRepository
from models.message import CreateMessagePayload
from services.agent_tour import AgentTourService
from repositories.tour import TourRepository

dotenv.load_dotenv()

router = APIRouter(prefix="/chat-bot", tags=["Chat Bot"])

# Lấy cấu hình model từ môi trường
config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY")
    }
]

# Schema để buộc model trả lời câu hỏi
function_schema = {
    "name": "chatbot_reply",
    "description": "Trả lời câu hỏi của người dùng về tour",
    "parameters": {
        "type": "object",
        "properties": {
            "response": {"type": "string"}
        },
        "required": ["response"]
    }
}

# Schema để trích xuất điểm đến
destination_extraction_schema = {
    "name": "extract_location",
    "description": "Trích xuất tên địa điểm từ văn bản đầu vào.",
    "parameters": {
        "type": "object",
        "properties": {
            "location_name": {
                "type": "string",
                "description": "Tên địa điểm được trích xuất"
            }
        },
        "required": ["location_name"]
    }
}

# Assistant Agent setup cho chatbot
agent = AssistantAgent(
    name="TourAssistant",
    system_message="""
Bạn là trợ lý AI chuyên tư vấn tour du lịch.
Bạn sẽ nhận được một câu hỏi từ người dùng và thông tin đuọc tìm thấy từ cơ sở dữ liệu.
- Nếu câu hỏi không liên quan đến tour du lịch, hãy trả lời một cách lịch sự và ngắn gọn.
- Nếu câu hỏi liên quan đến tour du lịch, hãy trả lời dựa trên thông tin đã tìm thấy.
- Nếu không tìm thấy thông tin nào, hãy trả lời rằng không có thông tin nào được tìm thấy.

Chỉ trả lời ngắn gọn, đúng trọng tâm. Trả lời bằng tiếng Việt.

""",
    llm_config={
        "config_list": config_list,
        "functions": [function_schema],
    }
)

# Assistant Agent setup cho trích xuất điểm đến
destination_agent = AssistantAgent(
    name="DestinationExtractor",
    system_message="""
Bạn là một trợ lý AI chuyên trích xuất địa điểm từ văn bản.
- Nếu tìm thấy địa điểm, chỉ trả về địa điểm đó dưới dạng chuỗi và không thêm bất cứ thứ gì.
- Nếu không tìm thấy địa điểm, không được trả lời gì cả.
""",
    llm_config={
        "config_list": config_list
    }
)

# Request model
class ChatbotRequest(BaseModel):
    chat_id: uuid.UUID
    message: str

@router.post("")
def chatbot_reply(request: ChatbotRequest):
    user_message = {"role": "user", "content": request.message}
    
    # 1️⃣ Trích xuất tour name từ nội dung
    try:
        tour_name = AgentTourService.extract_info_from_text(request.message)
        if not tour_name:
            tour_name = None
        print(f"✅ Tour name extracted: {tour_name}")
    except Exception as e:
        print(f"⚠️ Lỗi khi trích xuất tên tour: {str(e)}")
        tour_name = None

    # 2️⃣ Tìm tour cơ bản theo tên để lấy tour_id
    tour_basic_info = None
    if tour_name:
        try:
            tour_list = TourRepository.get_all_tour(tour_name)
            if tour_list:
                tour_basic_info = tour_list[0]  # lấy tour đầu tiên
            print(f"✅ Tour basic info: {tour_basic_info}")
        except Exception as e:
            print(f"⚠️ Lỗi khi tìm tour: {str(e)}")

    # 3️⃣ Dùng tour_id để truy xuất thông tin chi tiết
    tour_detail = None
    if tour_basic_info:
        try:
            tour_id = tour_basic_info.get("tour_id")
            tour_detail = TourRepository.get_tour_detail(tour_id)
            print(f"✅ Tour detail: {tour_detail}")
        except Exception as e:
            print(f"⚠️ Lỗi khi lấy chi tiết tour: {str(e)}")

    # 4️⃣ Lấy lịch sử chat
    try:
        chat_history = MessageRepository.get_recent_messages(chat_id=request.chat_id, limit=10)
    except Exception as e:
        print(f"⚠️ Lỗi khi lấy lịch sử chat: {str(e)}")
        chat_history = []

    # 5️⃣ Tạo input cho agent
    messages_to_agent = []
    if tour_detail:
        messages_to_agent.append({"role": "system", "content": f"Thông tin tour: {tour_detail}"})
    messages_to_agent.append(user_message)

    # 6️⃣ Gọi agent
    result = agent.generate_reply(messages=messages_to_agent)

    # 7️⃣ Xử lý kết quả agent
    answer = str(result)
    if isinstance(result, dict) and result.get("function_call"):
        args = result["function_call"].get("arguments")
        if args:
            try:
                response_json = json.loads(args)
                answer = response_json.get("response", "Xin lỗi, tôi chưa rõ ý bạn.")
            except:
                answer = "Xin lỗi, định dạng phản hồi không hợp lệ."

    # 8️⃣ Lưu tin nhắn user
    try:
        user_payload = CreateMessagePayload(chat_id=request.chat_id, content=request.message, role="user")
        MessageRepository.create(user_payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu tin nhắn user: {str(e)}")

    # 9️⃣ Lưu tin nhắn assistant
    try:
        assistant_payload = CreateMessagePayload(chat_id=request.chat_id, content=answer, role="assistant")
        MessageRepository.create(assistant_payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu tin nhắn assistant: {str(e)}")

    return {
        "reply": answer,
        "tour_name": tour_name,
        "tour_basic_info": tour_basic_info,
        "tour_detail": tour_detail,
        "message_id": str(request.chat_id)
    }
