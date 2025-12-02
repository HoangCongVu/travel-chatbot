import socketio
from typing import Dict, Set
import uuid

# Tạo Socket.IO server instance
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*', 
    logger=True,
    engineio_logger=True
)

# Thêm vào đầu file
admin_sessions: Set[str] = set()  # Track admin sessions

@sio.event
async def join_admin_room(sid):
    """Admin join vào room chung để nhận tất cả notifications"""
    try:
        await sio.enter_room(sid, "admin_room")
        admin_sessions.add(sid)
        print(f"👮 Admin {sid} joined admin room")
        print(f"📊 Total admins online: {len(admin_sessions)}")
        
        await sio.emit('joined_admin_room', {
            'message': 'Successfully joined admin room'
        }, room=sid)
        
    except Exception as e:
        print(f"❌ Error in join_admin_room: {e}")

@sio.event
async def leave_admin_room(sid):
    """Admin rời khỏi admin room"""
    try:
        await sio.leave_room(sid, "admin_room")
        if sid in admin_sessions:
            admin_sessions.remove(sid)
        print(f"👮 Admin {sid} left admin room")
        
    except Exception as e:
        print(f"❌ Error in leave_admin_room: {e}")

# Helper function - emit tới admin room
async def emit_admin_notification(notification_data: dict):
    """
    Broadcast notification đến TẤT CẢ admin đang online
    """
    await sio.emit('admin_notification', notification_data, room="admin_room")
    print(f"📢 Broadcasted admin notification: {notification_data.get('type')}")
    
# Lưu trữ mapping: chat_id -> set of session_ids
chat_rooms: Dict[str, Set[str]] = {}

@sio.event
async def connect(sid, environ, auth):
    """Khi client kết nối"""
    print(f"🔌 Client connected: {sid}")
    return True

@sio.event
async def disconnect(sid):
    """Khi client ngắt kết nối - UNIFIED"""
    print(f"🔌 Client disconnected: {sid}")
    
    # 1. Xóa khỏi admin sessions
    if sid in admin_sessions:
        admin_sessions.remove(sid)
        print(f"👮 Admin {sid} removed from admin room")
        print(f"📊 Total admins online: {len(admin_sessions)}")
    
    # 2. Xóa sid khỏi các chat room
    for chat_id, sessions in chat_rooms.items():
        if sid in sessions:
            sessions.remove(sid)
            print(f"📤 Client {sid} left chat room: {chat_id}")

@sio.event
async def join_chat(sid, data):
    """Client join vào một chat room cụ thể"""
    try:
        chat_id = data.get("chat_id")
        print(f"🔍 Received join_chat request: sid={sid}, chat_id={chat_id}")
        
        if not chat_id:
            await sio.emit('error', {'message': 'chat_id is required'}, room=sid)
            return
        
        # Validate UUID
        try:
            uuid.UUID(chat_id)
        except ValueError:
            await sio.emit('error', {'message': 'Invalid chat_id format'}, room=sid)
            return
        
        # ✅ AWAIT enter_room
        await sio.enter_room(sid, chat_id)  # ← THÊM AWAIT!
        
        # Lưu vào mapping
        if chat_id not in chat_rooms:
            chat_rooms[chat_id] = set()
        chat_rooms[chat_id].add(sid)
        
        print(f"✅ Client {sid} joined chat room: {chat_id}")
        print(f"📊 Room members: {chat_rooms[chat_id]}")
        
        await sio.emit('joined_chat', {
            'chat_id': chat_id,
            'message': 'Successfully joined chat room'
        }, room=sid)
        
    except Exception as e:
        print(f"❌ Error in join_chat: {e}")
        import traceback
        traceback.print_exc()

@sio.event
async def leave_chat(sid, data):
    """Client rời khỏi một chat room"""
    try:
        chat_id = data.get("chat_id")
        if not chat_id:
            return
        
        # ✅ AWAIT leave_room
        await sio.leave_room(sid, chat_id)  # ← THÊM AWAIT!
        
        if chat_id in chat_rooms and sid in chat_rooms[chat_id]:
            chat_rooms[chat_id].remove(sid)
        
        print(f"📤 Client {sid} left chat room: {chat_id}")
        await sio.emit('left_chat', {
            'chat_id': chat_id,
            'message': 'Left chat room'
        }, room=sid)
        
    except Exception as e:
        print(f"❌ Error in leave_chat: {e}")

@sio.event
async def send_message(sid, data):
    """
    Client gửi message qua socket (optional - có thể dùng REST API)
    data = {"chat_id": "uuid", "content": "text", "role": "user"}
    """
    try:
        chat_id = data.get("chat_id")
        content = data.get("content")
        role = data.get("role", "user")
        
        if not chat_id or not content:
            await sio.emit('error', {'message': 'chat_id and content are required'}, room=sid)
            return
        
        # Broadcast message đến tất cả clients trong room (trừ sender)
        await sio.emit('new_message', {
            'chat_id': chat_id,
            'content': content,
            'role': role,
            'timestamp': str(uuid.uuid1().time)
        }, room=chat_id, skip_sid=sid)
        
        print(f"📨 Message sent to room {chat_id}")
        
    except Exception as e:
        print(f"❌ Error in send_message: {e}")
        await sio.emit('error', {'message': str(e)}, room=sid)

# Helper functions để emit từ bên ngoài
# CẬP NHẬT hàm emit_new_message
async def emit_new_message(chat_id: str, message_data: dict):
    """
    Broadcast message mới đến:
    1. Tất cả clients trong chat room
    2. Tất cả admin (để update danh sách)
    """
    # Emit tới chat room
    await sio.emit('new_message', message_data, room=chat_id)
    print(f"📨 Broadcasted new message to room: {chat_id}")
    
    # Emit tới admin room
    await sio.emit('admin_notification', {
        'type': 'new_message',
        'chat_id': chat_id,
        'message': message_data
    }, room="admin_room")
    print(f"📢 Notified admins about new message in chat: {chat_id}")

async def emit_chat_update(chat_id: str, update_data: dict):
    """
    Broadcast chat update (title change, status, etc.)
    """
    await sio.emit('chat_updated', update_data, room=chat_id)
    print(f"🔄 Broadcasted chat update to room: {chat_id}")

async def emit_typing_indicator(chat_id: str, user_id: str, is_typing: bool):
    """
    Broadcast typing indicator
    """
    await sio.emit('typing', {
        'chat_id': chat_id,
        'user_id': user_id,
        'is_typing': is_typing
    }, room=chat_id)


# ============================================================================
# HELPER FUNCTION: Emit Socket Safely từ Sync Context
# ============================================================================

def emit_socket_safely(chat_id: str, message_data: dict):
    """
    Helper function để emit socket event an toàn từ sync context.
    Tự động xử lý event loop.
    
    Sử dụng cho:
    - Services chạy sync (chatbot_service, follow_up_settings, etc.)
    - Background jobs (APScheduler)
    - Bất kỳ nơi nào không có async context
    
    Args:
        chat_id: ID của chat room
        message_data: Dict chứa message data để emit
        
    Example:
        emit_socket_safely(str(chat_id), {
            "message_id": str(msg.id),
            "content": "Hello",
            "role": "assistant"
        })
    """
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Loop đang chạy → create task
            asyncio.create_task(emit_new_message(chat_id, message_data))
        else:
            # Loop không chạy → run to complete
            loop.run_until_complete(emit_new_message(chat_id, message_data))
    except RuntimeError:
        # Không có event loop → tạo mới
        try:
            asyncio.run(emit_new_message(chat_id, message_data))
        except Exception as e:
            print(f"⚠️ Socket emit failed: {e}")
