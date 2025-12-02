# 🚀 SOCKET.IO INTEGRATION - HƯỚNG DẪN ĐẦY ĐỦ

> **Travel Chatbot API - Real-time Chat System**  
> Socket.IO + FastAPI + Python

---

## 📋 MỤC LỤC

1. [Tổng Quan](#tổng-quan)
2. [Kiến Trúc Hệ Thống](#kiến-trúc-hệ-thống)
3. [Cài Đặt & Cấu Hình](#cài-đặt--cấu-hình)
4. [API Reference](#api-reference)
5. [Client Implementation](#client-implementation)
6. [Testing & Debugging](#testing--debugging)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## 📖 TỔNG QUAN

### Tính Năng Chính

✅ **Real-time messaging** - User, Admin, Chatbot giao tiếp tức thì  
✅ **Auto-reconnect** - Tự động kết nối lại khi mất kết nối  
✅ **Room-based** - Quản lý chat theo rooms (mỗi chat = 1 room)  
✅ **Multi-client** - Hỗ trợ nhiều clients cùng lúc trong 1 chat  
✅ **Follow-up messages** - Tin nhắn tự động real-time  
✅ **Admin panel** - Admin nhận thông báo real-time

### Stack Công Nghệ

- **Backend**: Python + FastAPI + Socket.IO (python-socketio)
- **Frontend**: JavaScript/TypeScript + socket.io-client
- **Protocol**: WebSocket (fallback: Long-polling)
- **Database**: PostgreSQL

---

## 🏗️ KIẾN TRÚC HỆ THỐNG

### Mô Hình "Củ Hành" (Onion Architecture)

```
┌─────────────────────────────────────────┐
│  FastAPI App (LỚP CORE)                 │
│  ├─ REST API: /api/*                    │
│  ├─ Controllers, Services, DB           │
│  └─ Socket.IO mounted at /socket.io    │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  Socket.IO Server                       │
│  ├─ WebSocket connections               │
│  ├─ Room management                     │
│  └─ Event broadcasting                  │
└─────────────────────────────────────────┘
```

### Flow Dữ Liệu

```
Client (Browser/Mobile)
    ↕ WebSocket
Socket.IO Server
    ↕ Python AsyncIO
FastAPI Backend
    ↕ SQLAlchemy
PostgreSQL Database
```

### Các Components Đã Tích Hợp

| Component              | File                             | Chức năng                          |
| ---------------------- | -------------------------------- | ---------------------------------- |
| **Socket Manager**     | `utils/socket_manager.py`        | Quản lý connections, rooms, events |
| **Chatbot Service**    | `services/chatbot_service.py`    | Emit messages từ AI chatbot        |
| **Follow-up Service**  | `services/follow_up_settings.py` | Emit messages tự động theo lịch    |
| **Chat Controller**    | `controllers/chat.py`            | Admin gửi message real-time        |
| **Message Controller** | `controllers/message.py`         | User gửi message real-time         |
| **Chatbot Controller** | `controllers/chatbot.py`         | User chat với AI real-time         |

---

## ⚙️ CÀI ĐẶT & CẤU HÌNH

### 1. Dependencies (Đã có trong project)

```toml
# pyproject.toml
dependencies = [
    "python-socketio[asyncio] (>=5.15.0,<6.0.0)",
    "fastapi[standard] (>=0.116.1,<0.117.0)",
    "uvicorn[standard] (>=0.35.0,<0.36.0)",
]
```

### 2. Server Configuration

**File: `utils/socket_manager.py`**

```python
import socketio
from typing import Dict, Set

# Tạo Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',  # Production: chỉ định domain cụ thể
    logger=True,
    engineio_logger=True
)

# Track rooms và sessions
chat_rooms: Dict[str, Set[str]] = {}
admin_sessions: Set[str] = set()
```

**File: `app.py`**

```python
from utils.socket_manager import sio

def create_app() -> FastAPI:
    app = FastAPI(title="Travel Chatbot API 🚀")

    # ... routes setup ...

    # 🔥 Mount Socket.IO
    socket_asgi_app = socketio.ASGIApp(
        socketio_server=sio,
        socketio_path=""
    )
    app.mount("/socket.io", socket_asgi_app)

    return app

app = create_app()
```

### 3. Chạy Server

```bash
# Development
poetry run fastapi dev app.py

# Hoặc với Uvicorn
poetry run uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Production
poetry run uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1
```

### 4. Endpoints

| Type          | URL                               | Mô tả                |
| ------------- | --------------------------------- | -------------------- |
| **Socket.IO** | `http://localhost:8000/socket.io` | WebSocket connection |
| **REST API**  | `http://localhost:8000/api/*`     | HTTP endpoints       |
| **Docs**      | `http://localhost:8000/docs`      | Swagger UI           |

---

## 📡 API REFERENCE

### Server Events (Server → Client)

| Event                | Trigger                     | Data Schema                                                   |
| -------------------- | --------------------------- | ------------------------------------------------------------- |
| `connect`            | Client kết nối thành công   | N/A                                                           |
| `disconnect`         | Client ngắt kết nối         | N/A                                                           |
| `joined_chat`        | Client join room thành công | `{chat_id, message}`                                          |
| `left_chat`          | Client rời room             | `{chat_id, message}`                                          |
| `new_message`        | Message mới được tạo        | `{message_id, chat_id, content, role, created_at, meta_data}` |
| `chat_updated`       | Chat metadata thay đổi      | `{chat_id, ...update_data}`                                   |
| `typing`             | User đang typing (optional) | `{chat_id, user_id, is_typing}`                               |
| `admin_notification` | Thông báo cho admin         | `{type, chat_id, message}`                                    |
| `error`              | Lỗi xảy ra                  | `{message}`                                                   |

### Client Events (Client → Server)

| Event              | Mục đích                          | Data Schema                | Response            |
| ------------------ | --------------------------------- | -------------------------- | ------------------- |
| `join_chat`        | Tham gia chat room                | `{chat_id: "uuid"}`        | `joined_chat`       |
| `leave_chat`       | Rời khỏi chat room                | `{chat_id: "uuid"}`        | `left_chat`         |
| `join_admin_room`  | Admin join vào admin room         | N/A                        | `joined_admin_room` |
| `leave_admin_room` | Admin rời admin room              | N/A                        | N/A                 |
| `send_message`     | Gửi message qua socket (optional) | `{chat_id, content, role}` | `new_message`       |

### REST API Endpoints

```bash
# User gửi message qua chatbot
POST /api/chat-bot
{
  "chat_id": "uuid",
  "message": "Tôi muốn đi Đà Lạt"
}
→ Auto emit: new_message (user) + new_message (assistant)

# Admin gửi message
POST /api/chats/{chat_id}/admin-message
Headers: Authorization: Bearer <admin-token>
{
  "content": "Xin chào, tôi có thể giúp gì?"
}
→ Auto emit: new_message (admin)

# Tạo message thủ công
POST /api/messages
{
  "chat_id": "uuid",
  "content": "Hello",
  "role": "user"
}
→ Auto emit: new_message
```

---

## 💻 CLIENT IMPLEMENTATION

### JavaScript/TypeScript (React)

#### Installation

```bash
npm install socket.io-client
# or
yarn add socket.io-client
```

#### Basic Usage

```typescript
import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";

const SOCKET_URL = "http://localhost:8000";

function ChatComponent({ chatId }: { chatId: string }) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [messages, setMessages] = useState<any[]>([]);

  useEffect(() => {
    // 1. Kết nối socket
    const socketInstance = io(SOCKET_URL, {
      path: "/socket.io",
      transports: ["websocket", "polling"],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    // 2. Xử lý connect
    socketInstance.on("connect", () => {
      console.log("✅ Connected:", socketInstance.id);
      socketInstance.emit("join_chat", { chat_id: chatId });
    });

    // 3. Xử lý join thành công
    socketInstance.on("joined_chat", (data) => {
      console.log("✅ Joined room:", data.chat_id);
    });

    // 4. Nhận message mới
    socketInstance.on("new_message", (data) => {
      console.log("📨 New message:", data);
      setMessages((prev) => [...prev, data]);
    });

    // 5. Xử lý lỗi
    socketInstance.on("error", (error) => {
      console.error("❌ Socket error:", error);
    });

    // 6. Xử lý disconnect
    socketInstance.on("disconnect", (reason) => {
      console.log("🔌 Disconnected:", reason);
    });

    // 7. Xử lý reconnect
    socketInstance.on("reconnect", (attemptNumber) => {
      console.log("🔄 Reconnected after", attemptNumber, "attempts");
    });

    setSocket(socketInstance);

    // Cleanup
    return () => {
      if (socketInstance) {
        socketInstance.emit("leave_chat", { chat_id: chatId });
        socketInstance.disconnect();
      }
    };
  }, [chatId]);

  const sendMessage = async (content: string) => {
    // Gửi qua REST API (recommended)
    const response = await fetch(`${SOCKET_URL}/api/chat-bot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: chatId,
        message: content,
      }),
    });
    // Server sẽ tự động emit 'new_message' event
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={msg.message_id || idx} className={`message ${msg.role}`}>
            <strong>{msg.role}:</strong> {msg.content}
            <span className="timestamp">{msg.created_at}</span>
          </div>
        ))}
      </div>
      <button onClick={() => sendMessage("Hello!")}>Send</button>
    </div>
  );
}

export default ChatComponent;
```

### Vue.js Example

```vue
<template>
  <div class="chat-container">
    <div
      v-for="message in messages"
      :key="message.message_id"
      :class="['message', message.role]"
    >
      <strong>{{ message.role }}:</strong> {{ message.content }}
    </div>
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { io } from "socket.io-client";

const props = defineProps({
  chatId: { type: String, required: true },
});

const socket = ref(null);
const messages = ref([]);

onMounted(() => {
  socket.value = io("http://localhost:8000", {
    path: "/socket.io",
  });

  socket.value.on("connect", () => {
    socket.value.emit("join_chat", { chat_id: props.chatId });
  });

  socket.value.on("new_message", (data) => {
    messages.value.push(data);
  });
});

onUnmounted(() => {
  if (socket.value) {
    socket.value.emit("leave_chat", { chat_id: props.chatId });
    socket.value.disconnect();
  }
});

const sendMessage = async () => {
  await fetch("http://localhost:8000/api/chat-bot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: props.chatId,
      message: "Hello from Vue!",
    }),
  });
};
</script>
```

### Python Client Example

```python
import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('✅ Connected to server')
    sio.emit('join_chat', {'chat_id': 'your-chat-uuid-here'})

@sio.event
def joined_chat(data):
    print(f'✅ Joined room: {data["chat_id"]}')

@sio.event
def new_message(data):
    print(f'📨 New message: {data["content"]} (from {data["role"]})')

@sio.event
def disconnect():
    print('🔌 Disconnected from server')

# Connect
sio.connect('http://localhost:8000', socketio_path='/socket.io')

# Wait
try:
    sio.wait()
except KeyboardInterrupt:
    sio.disconnect()
```

---

## 🧪 TESTING & DEBUGGING

### 1. Test với Browser Console

Mở DevTools Console và chạy:

```javascript
// 1. Load Socket.IO client
const script = document.createElement("script");
script.src = "https://cdn.socket.io/4.5.4/socket.io.min.js";
document.head.appendChild(script);

// 2. Sau khi load xong, connect
script.onload = () => {
  const socket = io("http://localhost:8000", {
    path: "/socket.io",
  });

  socket.on("connect", () => {
    console.log("✅ Connected:", socket.id);
    socket.emit("join_chat", { chat_id: "YOUR-CHAT-UUID" });
  });

  socket.on("joined_chat", (data) => {
    console.log("✅ Joined:", data);
  });

  socket.on("new_message", (data) => {
    console.log("📨 Message:", data);
  });

  socket.on("error", (error) => {
    console.error("❌ Error:", error);
  });

  // Lưu vào global để dùng sau
  window.testSocket = socket;
};

// 3. Test gửi message
// window.testSocket.emit('send_message', {
//   chat_id: 'YOUR-CHAT-UUID',
//   content: 'Test message',
//   role: 'user'
// });
```

### 2. Test với Postman/Thunder Client

1. Tạo WebSocket connection:
   - URL: `ws://localhost:8000/socket.io/?EIO=4&transport=websocket`
2. Gửi events:
   ```json
   ["join_chat", { "chat_id": "your-uuid" }]
   ```

### 3. Server Logs

Khi server chạy, bạn sẽ thấy:

```
Server initialized for asgi.         ← Socket.IO ready
✅ Database migrated to latest version.
INFO   Uvicorn running on http://127.0.0.1:8000

🔌 Client connected: abc123xyz       ← Client connect
🔍 Received join_chat request: ...   ← Join event
✅ Client joined chat room: uuid     ← Success
📊 Room members: {'abc123xyz'}       ← Room state

📨 Broadcasted new message to room: uuid  ← Message sent
```

### 4. Debug Helper Function

Thêm vào `utils/socket_manager.py`:

```python
def get_server_stats():
    """Get real-time server statistics"""
    return {
        "total_rooms": len(chat_rooms),
        "total_admins": len(admin_sessions),
        "rooms": {
            chat_id: len(sessions)
            for chat_id, sessions in chat_rooms.items()
        }
    }
```

---

## 🚀 PRODUCTION DEPLOYMENT

### 1. Security Configuration

**Update `utils/socket_manager.py`:**

```python
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[
        'https://yourdomain.com',
        'https://admin.yourdomain.com'
    ],
    logger=False,  # Tắt verbose logging
    engineio_logger=False,
    ping_timeout=60,
    ping_interval=25
)
```

### 2. Environment Variables

```bash
# .env
SOCKET_IO_CORS_ORIGINS=https://yourdomain.com,https://admin.yourdomain.com
SOCKET_IO_PING_TIMEOUT=60
SOCKET_IO_PING_INTERVAL=25
```

### 3. Scaling với Redis

**Install:**

```bash
poetry add redis aioredis
```

**Config:**

```python
import socketio

# Redis manager cho multiple server instances
sio = socketio.AsyncServer(
    async_mode='asgi',
    client_manager=socketio.AsyncRedisManager(
        'redis://localhost:6379'
    )
)
```

### 4. Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install poetry
RUN poetry install --no-dev

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5. Nginx Reverse Proxy

```nginx
upstream fastapi_backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://fastapi_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /socket.io/ {
        proxy_pass http://fastapi_backend/socket.io/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_buffering off;
    }
}
```

---

## 🐛 TROUBLESHOOTING

### ❌ Lỗi: "no running event loop" / "coroutine was never awaited"

**Triệu chứng:**

```
RuntimeWarning: coroutine 'emit_new_message' was never awaited
⚠️ Socket emit failed: no running event loop
```

**Nguyên nhân:** Gọi async function từ sync context

**✅ Giải pháp:** Dùng `emit_socket_safely()` từ `utils/socket_manager.py`

```python
from utils.socket_manager import emit_socket_safely

# Thay vì:
await emit_new_message(chat_id, data)  # ❌ Lỗi trong sync context

# Dùng:
emit_socket_safely(chat_id, data)  # ✅ OK
```

### ❌ Connection Failed

**Kiểm tra:**

1. Server đang chạy:

   ```bash
   curl http://localhost:8000/
   ```

2. Socket.IO path đúng: `/socket.io`

   ```javascript
   io("http://localhost:8000", { path: "/socket.io" });
   ```

3. CORS configuration:
   ```python
   # Cho phép origin của client
   cors_allowed_origins=['http://localhost:3000']
   ```

### ❌ Messages Không Nhận Được

**Checklist:**

- [ ] Đã gọi `socket.emit('join_chat', {chat_id})` chưa?
- [ ] `chat_id` có phải valid UUID không?
- [ ] Check server logs có thấy `joined_chat` không?
- [ ] Listener `socket.on('new_message')` đã setup chưa?

### ❌ Multiple Message Duplicates

**Nguyên nhân:** User message bị emit 2 lần (controller + service)

**✅ Giải pháp:** Đã fix - Chỉ emit ở controller, service không emit user message

---

## ✨ BEST PRACTICES

### 1. Connection Management

```javascript
// ✅ ĐÚNG: Cleanup khi unmount
useEffect(() => {
  const socket = io(SOCKET_URL);

  return () => {
    socket.disconnect(); // Cleanup
  };
}, []);

// ❌ SAI: Không cleanup → memory leak
useEffect(() => {
  const socket = io(SOCKET_URL);
  // Missing cleanup!
}, []);
```

### 2. Error Handling

```javascript
socket.on("error", (error) => {
  console.error("Socket error:", error);
  // Show user-friendly message
  toast.error("Connection error. Please try again.");
});

socket.on("connect_error", (error) => {
  console.error("Connection error:", error);
  // Retry logic hoặc fallback
});
```

### 3. Message Deduplication

```javascript
const [messages, setMessages] = useState([]);
const [messageIds, setMessageIds] = useState(new Set());

socket.on("new_message", (data) => {
  if (!messageIds.has(data.message_id)) {
    setMessages((prev) => [...prev, data]);
    setMessageIds((prev) => new Set([...prev, data.message_id]));
  }
});
```

### 4. Rate Limiting (Server)

```python
from collections import defaultdict
from time import time

message_counts = defaultdict(list)
RATE_LIMIT = 10  # messages
TIME_WINDOW = 60  # seconds

@sio.event
async def send_message(sid, data):
    now = time()
    # Cleanup old timestamps
    message_counts[sid] = [
        ts for ts in message_counts[sid]
        if now - ts < TIME_WINDOW
    ]

    # Check limit
    if len(message_counts[sid]) >= RATE_LIMIT:
        await sio.emit('error', {
            'message': 'Rate limit exceeded'
        }, room=sid)
        return

    message_counts[sid].append(now)
    # Process message...
```

### 5. Authentication

```javascript
// Client: Gửi token khi connect
const socket = io(SOCKET_URL, {
  auth: {
    token: localStorage.getItem("access_token"),
  },
});
```

```python
# Server: Verify token
@sio.event
async def connect(sid, environ, auth):
    token = auth.get('token')
    if not verify_token(token):
        return False  # Reject connection
    return True
```

### 6. Logging & Monitoring

```python
import logging

logger = logging.getLogger(__name__)

@sio.event
async def connect(sid, environ, auth):
    logger.info(f"Client connected: {sid}")
    # Log to monitoring service (Sentry, DataDog, etc.)
```

### 7. Graceful Shutdown

```python
import signal
import sys

def shutdown_handler(signum, frame):
    logger.info("Shutting down gracefully...")
    # Notify all connected clients
    asyncio.run(sio.emit('server_shutdown', {
        'message': 'Server is restarting'
    }))
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)
```

---

## 📊 PERFORMANCE OPTIMIZATION

### 1. Message Batching

Thay vì emit từng message, batch multiple updates:

```python
pending_messages = []

async def emit_batch():
    if pending_messages:
        await sio.emit('message_batch', pending_messages)
        pending_messages.clear()

# Schedule batch emit every 100ms
```

### 2. Connection Pooling

```python
# Limit concurrent connections per user
max_connections_per_user = 5

@sio.event
async def connect(sid, environ, auth):
    user_id = auth.get('user_id')
    user_connections = get_user_connections(user_id)

    if len(user_connections) >= max_connections_per_user:
        return False  # Reject
```

### 3. Compression

```python
sio = socketio.AsyncServer(
    async_mode='asgi',
    compression_threshold=1024  # Compress messages > 1KB
)
```

---

## 🎯 CHECKLIST HOÀN TẤT

### Server Setup

- [x] Socket.IO server configured trong `utils/socket_manager.py`
- [x] Mounted vào FastAPI trong `app.py`
- [x] Helper function `emit_socket_safely()` cho sync context
- [x] Admin room management
- [x] Chat room management

### Controllers Integration

- [x] `controllers/chat.py` - Admin messages
- [x] `controllers/message.py` - User messages
- [x] `controllers/chatbot.py` - Chatbot messages

### Services Integration

- [x] `services/chatbot_service.py` - AI responses
- [x] `services/follow_up_settings.py` - Scheduled messages

### Testing

- [x] Server khởi động thành công
- [ ] Client connect thành công
- [ ] Join/leave chat rooms
- [ ] Receive new messages
- [ ] Admin notifications
- [ ] Follow-up messages
- [ ] Multiple clients support
- [ ] Reconnection handling

### Production Ready

- [ ] CORS configured cho production domains
- [ ] Authentication implemented
- [ ] Rate limiting enabled
- [ ] Error logging setup
- [ ] Monitoring integrated
- [ ] Redis adapter (nếu scale)
- [ ] Load balancer configured
- [ ] SSL/TLS enabled

---

## 📚 TÀI LIỆU THAM KHẢO

- [Socket.IO Documentation](https://socket.io/docs/v4/)
- [python-socketio](https://python-socketio.readthedocs.io/)
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [socket.io-client](https://socket.io/docs/v4/client-api/)

---

## 🤝 SUPPORT

Nếu gặp vấn đề, check:

1. **Server logs**: `poetry run fastapi dev app.py`
2. **Browser console**: DevTools → Console tab
3. **Network tab**: Check WebSocket connections
4. **File này**: Phần Troubleshooting ở trên

---

**Cập nhật lần cuối**: 02/12/2025  
**Version**: 1.0  
**Author**: Travel Chatbot Team
