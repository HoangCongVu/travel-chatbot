from fastapi import APIRouter, Request, HTTPException
import json
import uuid
from env import env
from services.chatbot_service import ChatbotService
from services.chat import ChatService
from services.message import MessageService
from models.chat import CreateChatPayload
from models.message import CreateMessagePayload
import httpx
import asyncio 

router = APIRouter(tags=["Facebook Webhook"])

# Verify Token và Access Token
VERIFY_TOKEN = env.VERIFY_TOKEN
PAGE_ACCESS_TOKEN = env.PAGE_ACCESS_TOKEN


async def get_or_create_chat_for_facebook_user(facebook_user_id: str) -> uuid.UUID:
    """
    Tìm hoặc tạo chat session cho Facebook user.
    Sử dụng platform='facebook' và external_user_id=facebook_user_id để tìm trong DB.
    """
    platform_name = "facebook"
    
    # 1. Thử tìm chat cũ trong DB
    try:
        existing_chat = ChatService.find_by_platform_id(
            platform=platform_name, 
            external_id=facebook_user_id
        )
        
        if existing_chat:
            print(f"✅ Found existing chat {existing_chat.id} for Facebook user {facebook_user_id}")
            return existing_chat.id
            
    except Exception as e:
        print(f"🔍 Chat not found for {facebook_user_id}, will create new one")

    # 2. Nếu không có, tạo chat mới
    try:
        chat_payload = CreateChatPayload(
            title=f"Facebook Chat - {facebook_user_id}",
            session_id=uuid.uuid4(),
            platform=platform_name,
            external_user_id=facebook_user_id
        )
        
        chat = ChatService.create_chat(chat_payload)
        
        print(f"✅ Created new chat session {chat.id} for Facebook user {facebook_user_id}")
        return chat.id
        
    except Exception as e:
        print(f"❌ Error creating chat for Facebook user {facebook_user_id}: {e}")
        raise


@router.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode and token:
        print(f"🔍 Facebook Verification request")
        print(f"   Mode: {mode}, Token: {token}, Challenge: {challenge}")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ WEBHOOK_VERIFIED - Returning challenge")
            try:
                return int(challenge)
            except (ValueError, TypeError):
                return challenge
        else:
            raise HTTPException(status_code=403, detail="Verification token mismatch")
    
    return {
        "service": "Facebook Webhook",
        "status": "active",
        "message": "Webhook verification & event handling",
        "docs": "/docs"
    }


@router.post("/webhook")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    print("📩 Received Webhook Data:", json.dumps(data, indent=2, ensure_ascii=False))

    if data.get("object") != "page":
        return {"status": "ok"}

    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            sender_id = event.get("sender", {}).get("id")
            recipient_id = event.get("recipient", {}).get("id")

            # Xử lý tin nhắn text
            if "message" in event:
                message_text = event["message"].get("text", "")
                if not message_text:
                    continue

                print(f"💬 Message from {sender_id}: {message_text}")
                
                try:
                    # 1. Tạo hoặc lấy chat session
                    chat_id = await get_or_create_chat_for_facebook_user(sender_id)
                    print(f"✅ Chat ID: {chat_id}")

                    # 2. Gọi chatbot (ChatbotService sẽ tự động lưu tin nhắn)
                    bot_response = ChatbotService.process_chat(chat_id, message_text)
                    bot_reply = bot_response.get("reply", "Xin lỗi, tôi không hiểu câu hỏi của bạn.")
                    print(f"🤖 Bot reply ({len(bot_reply)} chars):")
                    print(bot_reply)
                    print("="*50)

                    # 3. Gửi phản hồi qua Facebook
                    await send_facebook_message(sender_id, bot_reply)
                    print(f"✅ Successfully replied to {sender_id}")

                except Exception as e:
                    import traceback
                    print(f"❌ Error processing message from {sender_id}: {e}")
                    print(traceback.format_exc())
                    await send_facebook_message(sender_id, "Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.")

            # Xử lý postback
            elif "postback" in event:
                payload = event["postback"].get("payload", "")
                print(f"🔘 Postback from {sender_id}: {payload}")
                # TODO: xử lý postback

    return {"status": "ok"}


async def send_facebook_message(recipient_id: str, message_text: str):
    url = "https://graph.facebook.com/v21.0/me/messages"
    headers = {"Content-Type": "application/json"}
    params = {"access_token": PAGE_ACCESS_TOKEN}

    MAX_LENGTH = 2000
    messages = []

    # --- Bỏ qua nếu tin nhắn trống ---
    if not message_text or not message_text.strip():
        return {"status": "skipped", "reason": "Empty message"}

    # --- Chia nhỏ tin nhắn dài ---
    while message_text:
        if len(message_text) <= MAX_LENGTH:
            messages.append(message_text.strip())
            break

        split_at = -1
        pos_n = message_text.rfind('\n', 0, MAX_LENGTH)
        pos_dot = message_text.rfind('. ', 0, MAX_LENGTH)

        if pos_n != -1:
            split_at = pos_n + 1
        elif pos_dot != -1:
            split_at = pos_dot + 2
        else:
            pos_space = message_text.rfind(' ', 0, MAX_LENGTH)
            split_at = pos_space + 1 if pos_space != -1 else MAX_LENGTH

        messages.append(message_text[:split_at].strip())
        message_text = message_text[split_at:].strip()

        if len(messages) >= 10:
            print(f"⚠️ Warning: Message for {recipient_id} split into more than 10 parts, truncating.")
            break

    # --- Gửi tin nhắn ---
    messages_sent = 0
    timeout = httpx.Timeout(20.0, connect=10.0, read=10.0)  # tăng timeout tổng 20s

    async with httpx.AsyncClient(timeout=timeout) as client:
        for i, msg in enumerate(messages):
            if not msg:
                continue

            payload = {
                "recipient": {"id": recipient_id},
                "message": {"text": msg},
                "messaging_type": "RESPONSE"
            }

            # Retry logic: thử lại tối đa 3 lần nếu lỗi mạng
            for attempt in range(3):
                try:
                    response = await client.post(url, json=payload, headers=headers, params=params)
                    response.raise_for_status()

                    print(f"✅ Sent part {i+1}/{len(messages)} to {recipient_id}: {response.status_code}")
                    messages_sent += 1

                    # Thêm độ trễ nhỏ giữa các phần tin nhắn
                    if len(messages) > 1:
                        await asyncio.sleep(1)
                    break  # thành công, thoát retry

                except httpx.ConnectTimeout:
                    print(f"⚠️ Connect timeout (attempt {attempt+1}/3) sending to {recipient_id}")
                    if attempt == 2:
                        print("❌ Gửi thất bại sau 3 lần thử (ConnectTimeout).")
                        return {"status": "failed", "error": "connect_timeout"}
                    await asyncio.sleep(2)

                except httpx.HTTPStatusError as e:
                    print(f"❌ HTTP error {e.response.status_code}: {e.response.text}")
                    # Nếu token sai hoặc lỗi quyền => không retry nữa
                    return {"status": "failed", "error": f"http_{e.response.status_code}"}

                except httpx.RequestError as e:
                    print(f"❌ Network error sending to {recipient_id}: {e}")
                    if attempt == 2:
                        return {"status": "failed", "error": "network_error"}
                    await asyncio.sleep(2)

    return {"status": "success", "messages_sent": messages_sent}