from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, json, dotenv
from autogen import AssistantAgent
import uuid
from repositories.message import MessageRepository
from models.message import CreateMessagePayload
# from controllers.sementic_search import search_tour_by_embedding, search_tour_by_destination


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
    
    # Bước 1: Thử trích xuất điểm đến trước
    try:
        extraction_result = destination_agent.generate_reply(
            messages=[user_message],
            function_call={"name": "extract_location"}
        )
        print("🧠 extraction_result:", extraction_result)
    except Exception as e:
        print(f"⚠️ Lỗi khi trích xuất điểm đến: {str(e)}")
        extraction_result = None

    print(f"✅ Điểm đến được trích xuất: {extraction_result}")

    # Bước 2: Nếu có điểm đến, thực hiện tìm kiếm thông tin tour
    search_info = None
    if extraction_result:
        try:
            search_info = search_tour_by_destination(extraction_result)[0]
        except Exception as e:
            print(f"⚠️ Lỗi khi tìm kiếm tour: {str(e)}")
    print(f"✅ Thông tin tour tìm được: {search_info}")

    # Bước 3: Lấy lịch sử chat (10 tin nhắn gần nhất)
    try:
        chat_history = MessageRepository.get_recent_messages(chat_id=request.chat_id, limit=10)
        print(f"🧠 Lịch sử chat: {chat_history}")
    except Exception as e:
        print(f"⚠️ Lỗi khi lấy lịch sử chat: {str(e)}")
        chat_history = []

    # Bước 4: Tạo input cho agent từ lịch sử chat và thông tin mới
    messages_to_agent = []
    # for message in chat_history:
    # # Đảm bảo role hợp lệ trước khi thêm
    #     if message.role in ["system", "assistant", "user", "function", "tool", "developer"]:
    #         messages_to_agent.append({"role": message.role, "content": message.content})
    #     else:
    #         print(f"⚠️ Tin nhắn với role không hợp lệ: {message.role}")

    # Nếu có thông tin tìm kiếm, thêm vào trước tin nhắn của người dùng
    if search_info:
        messages_to_agent.append({"role": "system", "content": f"Thông tin tour tìm được: {str(search_info)}"})

    # Thêm tin nhắn mới của người dùng vào cuối
    messages_to_agent.append(user_message)
    print(f"✅ Tin nhắn gửi đến agent: {messages_to_agent}")

    # Bước 5: Gọi agent để lấy câu trả lời
    result = agent.generate_reply(messages=messages_to_agent)
    print("🧠 agent_result:", result)

    if isinstance(result, dict) and result.get("function_call"):
        args = result["function_call"].get("arguments")
        if args:
            try:
                response_json = json.loads(args)
                answer = response_json.get("response", "Xin lỗi, tôi chưa rõ ý bạn.")
            except Exception as e:
                print(f"Lỗi khi parse JSON trả lời: {str(e)}")
                answer = "Xin lỗi, định dạng phản hồi không hợp lệ."
        else:
            answer = "Xin lỗi, tôi chưa rõ ý bạn."
    else:
        answer = str(result)

    # Bước 6: Kiểm tra chat có tồn tại không
    try:
        from repositories.chat import ChatRepository
        chat = ChatRepository.get_one(request.chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail=f"Chat với ID {request.chat_id} không tồn tại")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Chat với ID {request.chat_id} không tồn tại: {str(e)}")

    # Bước 7: Lưu tin nhắn của người dùng
    try:
        user_payload = CreateMessagePayload(
            chat_id=request.chat_id,
            content=request.message,
            role="user",  # Vai trò là user
        )
        MessageRepository.create(user_payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu tin nhắn của người dùng: {str(e)}")

    # Bước 8: Lưu tin nhắn của chatbot
    try:
        chatbot_payload = CreateMessagePayload(
            chat_id=request.chat_id,
            content=answer,
            role="assistant",  # Vai trò là admin
        )
        MessageRepository.create(chatbot_payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu tin nhắn của chatbot: {str(e)}")

    return {"reply": answer, "destination": extraction_result, "message_id": str(request.chat_id)}