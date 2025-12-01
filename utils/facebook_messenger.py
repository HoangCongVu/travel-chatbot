"""
Utils để gửi tin nhắn lên Facebook Messenger
"""
import httpx
import asyncio
from env import env

PAGE_ACCESS_TOKEN = env.PAGE_ACCESS_TOKEN


async def send_facebook_message(recipient_id: str, message_text: str) -> dict:
    """
    Gửi tin nhắn lên Facebook Messenger
    
    Args:
        recipient_id: Facebook User ID (external_user_id)
        message_text: Nội dung tin nhắn
        
    Returns:
        Dict chứa status: 'success' hoặc 'failed'
    """
    url = "https://graph.facebook.com/v21.0/me/messages"
    headers = {"Content-Type": "application/json"}
    params = {"access_token": PAGE_ACCESS_TOKEN}

    MAX_LENGTH = 2000
    messages = []

    # Bỏ qua nếu tin nhắn trống
    if not message_text or not message_text.strip():
        return {"status": "skipped", "reason": "Empty message"}

    # Chia nhỏ tin nhắn dài
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
            print(f"⚠️ Warning: Message split into more than 10 parts, truncating.")
            break

    # Gửi tin nhắn
    messages_sent = 0
    timeout = httpx.Timeout(20.0, connect=10.0, read=10.0)

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

                    print(f"✅ Sent Facebook message part {i+1}/{len(messages)} to {recipient_id}: {response.status_code}")
                    messages_sent += 1

                    # Thêm độ trễ nhỏ giữa các phần tin nhắn
                    if len(messages) > 1:
                        await asyncio.sleep(1)
                    break  # thành công, thoát retry

                except httpx.ConnectTimeout:
                    print(f"⚠️ Connect timeout (attempt {attempt+1}/3) sending to {recipient_id}")
                    if attempt == 2:
                        print("❌ Failed after 3 attempts (ConnectTimeout).")
                        return {"status": "failed", "error": "connect_timeout"}
                    await asyncio.sleep(2)

                except httpx.HTTPStatusError as e:
                    print(f"❌ HTTP error {e.response.status_code}: {e.response.text}")
                    return {"status": "failed", "error": f"http_{e.response.status_code}"}

                except httpx.RequestError as e:
                    print(f"❌ Network error sending to {recipient_id}: {e}")
                    if attempt == 2:
                        return {"status": "failed", "error": "network_error"}
                    await asyncio.sleep(2)

    return {"status": "success", "messages_sent": messages_sent}
