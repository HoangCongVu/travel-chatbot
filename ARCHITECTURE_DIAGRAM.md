# SƠ ĐỒ KIẾN TRÚC TRAVEL CHATBOT

## 📊 Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRAVEL CHATBOT SYSTEM                                │
│                    (Multi-Agent RAG Architecture)                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  📱 Web App        💬 Facebook Messenger        📧 Email/SMS                 │
│           └──────────────┬───────────────────────┘                           │
│                          │                                                    │
│                     [WebSocket/HTTP]                                         │
└──────────────────────────┼──────────────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────────────┐
│                        API GATEWAY LAYER                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃                        FastAPI Application                            ┃  │
│  ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫  │
│  ┃  • app.py - Main application                                         ┃  │
│  ┃  • CORS Middleware                                                    ┃  │
│  ┃  • Authentication Middleware                                          ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│                                                                               │
│  ┌─────────────────────┐          ┌──────────────────────┐                  │
│  │  REST API Routes    │          │  Socket.IO Server    │                  │
│  │  (/api/*)           │          │  (Real-time Chat)    │                  │
│  └──────────┬──────────┘          └──────────┬───────────┘                  │
└─────────────┼──────────────────────────────────┼──────────────────────────────┘
              │                                  │
┌─────────────▼──────────────────────────────────▼──────────────────────────────┐
│                         CONTROLLER LAYER                                      │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌──────────────┐  ┌───────────┐  ┌──────────┐  ┌──────────────┐            │
│  │ chatbot.py   │  │ chat.py   │  │ user.py  │  │ bookings.py  │            │
│  │ - POST /     │  │ - CRUD    │  │ - Auth   │  │ - CRUD       │            │
│  └──────┬───────┘  └─────┬─────┘  └────┬─────┘  └──────┬───────┘            │
│         │                │              │                │                     │
│  ┌──────┴────────────────┴──────────────┴────────────────┴───────┐           │
│  │  facebook_webhook.py  │  payment_webhook.py  │  agent_tour.py │           │
│  │  - FB Messenger       │  - Payment Gateway   │  - Upload Files│           │
│  └─────────────────────────────────────────────────────────────────           │
│                                                                                │
└────────────────────────────────┬───────────────────────────────────────────────┘
                                 │
┌────────────────────────────────▼───────────────────────────────────────────────┐
│                           SERVICE LAYER                                        │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃                    🤖 CHATBOT SERVICE (CORE)                             ┃  │
│  ┃                     chatbot_service.py                                   ┃  │
│  ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫  │
│  ┃                                                                           ┃  │
│  ┃  process_chat(chat_id, user_message)                                     ┃  │
│  ┃    1. Get chat history + tour context                                    ┃  │
│  ┃    2. Create Multi-Agent system                                          ┃  │
│  ┃    3. Execute GroupChat                                                  ┃  │
│  ┃    4. Extract answer & metadata                                          ┃  │
│  ┃    5. Save message & emit Socket.IO                                      ┃  │
│  ┃                                                                           ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│                                 │                                              │
│                                 ▼                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │              🎭 MULTI-AGENT SYSTEM (AutoGen)                           │  │
│  │                    agents/chatbot_agents.py                            │  │
│  ├────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                         │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │  1️⃣ IntelligentCoordinator (Lễ Tân)                             │ │  │
│  │  │     • Phân loại tin nhắn: đơn giản vs phức tạp                   │ │  │
│  │  │     • Xử lý chào hỏi, SĐT, spam                                  │ │  │
│  │  │     • Route yêu cầu phức tạp → PlannerAgent                      │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  │                                   ↓                                     │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │  2️⃣ PlannerAgent (Nhạc Trưởng)                                  │ │  │
│  │  │     • Phân tích yêu cầu người dùng                               │ │  │
│  │  │     • Lập kế hoạch (search tour hoặc web search)                 │ │  │
│  │  │     • Gọi tools thông qua UserProxy                              │ │  │
│  │  │     • Điều phối luồng xử lý                                      │ │  │
│  │  │                                                                   │ │  │
│  │  │     Tools Available:                                             │ │  │
│  │  │     ├─ search_tour_chat()                                        │ │  │
│  │  │     └─ search_web_information()                                  │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  │                                   ↓                                     │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │  3️⃣ UserProxy (Thực Thi)                                        │ │  │
│  │  │     • Execute function calls                                     │ │  │
│  │  │     • Return tool results                                        │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  │                                   ↓                                     │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │  4️⃣ RecommendationAgent (Tư Vấn Viên)                           │ │  │
│  │  │     • Tổng hợp kết quả từ tools                                  │ │  │
│  │  │     • Phân tích và so sánh tours                                 │ │  │
│  │  │     • Tạo câu trả lời FINAL_ANSWER                               │ │  │
│  │  │     • Tư vấn và gợi ý tour phù hợp                               │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                         │  │
│  │  GroupChatManager: Điều phối 4 agents theo auto speaker selection     │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  🔍 SEARCH SERVICES                                                     │  │
│  │  ├─ tour_search.py - Search tours from database                        │  │
│  │  │  • search_tour_chat(destination, min/max_price, target_date)        │  │
│  │  │  • search_tour_by_destination()                                     │  │
│  │  │  • search_tour_in_month()                                           │  │
│  │  │                                                                      │  │
│  │  └─ web_search.py - Real-time web search                               │  │
│  │     • search_web_information(query) → Google/Bing API                  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  💼 BUSINESS SERVICES                                                   │  │
│  │  • message.py - Message CRUD                                            │  │
│  │  • chat.py - Chat session management                                    │  │
│  │  • bookings.py - Booking management                                     │  │
│  │  • payments.py - Payment processing                                     │  │
│  │  • follow_up_settings.py - Auto follow-up config                        │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────┬───────────────────────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────────────────────┐
│                        REPOSITORY LAYER (Data Access)                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  • tour.py               • tour_departure.py        • tour_destination.py       │
│  • price_by_package.py   • price_by_date.py         • visa_price.py            │
│  • departure_schedule.py • recurring_schedule.py    • specific_departure.py    │
│  • user.py               • chat.py                  • message.py               │
│  • bookings.py           • carts.py                 • cart_items.py            │
│  • payments.py           • follow_up_settings.py                               │
│                                                                                  │
│  All using: SQLAlchemy ORM + PostgreSQL                                        │
└─────────────────────────────────┬───────────────────────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────────────────────┐
│                           DATABASE LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃                         PostgreSQL Database                              ┃  │
│  ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫  │
│  ┃                                                                           ┃  │
│  ┃  Tables:                                                                  ┃  │
│  ┃  • users                 • chats                 • messages              ┃  │
│  ┃  • tours                 • tour_departures       • tour_destinations     ┃  │
│  ┃  • tour_types            • tour_highlight_locations                      ┃  │
│  ┃  • departure_schedules   • recurring_schedules   • specific_departures   ┃  │
│  ┃  • price_by_packages     • price_by_dates        • visa_prices           ┃  │
│  ┃  • bookings              • carts                 • cart_items            ┃  │
│  ┃  • payments              • follow_up_settings    • files                 ┃  │
│  ┃                                                                           ┃  │
│  ┃  Migration: Alembic                                                       ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL INTEGRATIONS                                    │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  🤖 LLM API              🔍 Web Search API         💳 Payment Gateway            │
│  • OpenAI GPT            • Google Search           • VNPay/MoMo                  │
│  • Claude (Anthropic)    • Bing Search             • Webhook callbacks          │
│                                                                                   │
│  📱 Social Media         📧 Notifications                                        │
│  • Facebook Messenger    • Email Service (SMTP)                                  │
│  • Webhook Integration   • SMS Service                                           │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 LUỒNG XỬ LÝ CHATBOT (Message Flow)

```
┌───────────┐
│   USER    │
│ 💬 Message│
└─────┬─────┘
      │
      │ 1. Send message (HTTP/WebSocket)
      ▼
┌─────────────────────────────────────┐
│  Controller: chatbot.py             │
│  POST /api/chat-bot/                │
│  • Validate request                 │
│  • Save user message                │
│  • Emit Socket.IO event             │
└──────────────┬──────────────────────┘
               │
               │ 2. Call process_chat()
               ▼
┌─────────────────────────────────────────────────────────────┐
│  Service: chatbot_service.py                                │
│  • Get chat history (recent 10 messages)                    │
│  • Get tour context (last tour search in conversation)      │
│  • Format context message                                   │
└──────────────┬──────────────────────────────────────────────┘
               │
               │ 3. Initialize Multi-Agent System
               ▼
┌─────────────────────────────────────────────────────────────┐
│  🎭 MULTI-AGENT ORCHESTRATION                               │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Step 1: IntelligentCoordinator receives message  │    │
│  │  ├─ Is greeting/phone/spam?                        │    │
│  │  │  └─ YES → Return FINAL_ANSWER directly          │    │
│  │  └─ Complex request (find tour, ask about place)?  │    │
│  │     └─ YES → Route to PlannerAgent                 │    │
│  └────────────────────────────────────────────────────┘    │
│                           ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Step 2: PlannerAgent analyzes request            │    │
│  │  ├─ Need tour search?                              │    │
│  │  │  └─ Call search_tour_chat() via UserProxy      │    │
│  │  ├─ Need web information?                          │    │
│  │  │  └─ Call search_web_information() via UserProxy│    │
│  │  └─ Get tool results                               │    │
│  └────────────────────────────────────────────────────┘    │
│                           ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Step 3: UserProxy executes function calls         │    │
│  │  • search_tour_chat() → TourSearchService          │    │
│  │  • search_web_information() → WebSearchService     │    │
│  │  • Return results to PlannerAgent                  │    │
│  └────────────────────────────────────────────────────┘    │
│                           ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Step 4: RecommendationAgent processes results     │    │
│  │  • Analyze tour options                            │    │
│  │  • Compare prices, dates, highlights               │    │
│  │  • Generate FINAL_ANSWER with recommendations      │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  GroupChatManager: Auto select speaker, max 15 rounds      │
└──────────────┬───────────────────────────────────────────────┘
               │
               │ 4. Extract results
               ▼
┌─────────────────────────────────────────────────────────────┐
│  Service: chatbot_service.py                                │
│  • Extract FINAL_ANSWER from messages                       │
│  • Extract tour_detail from tool results                    │
│  • Extract metadata (tours JSON)                            │
└──────────────┬──────────────────────────────────────────────┘
               │
               │ 5. Save & Emit
               ▼
┌─────────────────────────────────────────────────────────────┐
│  • Save assistant message to database                       │
│  • Include meta_data (tour search results)                  │
│  • Emit Socket.IO event to client                           │
│  • Return response                                          │
└─────────────────────────────────────────────────────────────┘
               │
               │ 6. Real-time update
               ▼
┌───────────┐
│   USER    │
│ 📱 Receive│
└───────────┘
```

---

## 🔍 TOUR SEARCH ARCHITECTURE (RAG Component)

```
┌──────────────────────────────────────────────────────────────┐
│         🔍 TOUR SEARCH SERVICE (Retrieval Component)         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  search_tour_chat(destination, min_price, max_price,         │
│                   target_date, limit)                        │
│                                                               │
│  1️⃣ SEARCH PHASE                                            │
│     ├─ Search by destination text (FTS)                      │
│     ├─ Filter by price range                                 │
│     ├─ Filter by available dates                             │
│     └─ Limit results                                         │
│                                                               │
│  2️⃣ ENRICHMENT PHASE (for each tour)                        │
│     ├─ Get tour basic info                                   │
│     ├─ Get departures (tour_departures)                      │
│     ├─ Get destinations (tour_destinations)                  │
│     ├─ Get highlight locations                               │
│     ├─ Get departure schedules:                              │
│     │  ├─ Recurring schedules (weekly/monthly)               │
│     │  └─ Specific departure dates                           │
│     ├─ Get prices:                                           │
│     │  ├─ Visa prices                                        │
│     │  ├─ Price by packages                                  │
│     │  └─ Price by dates                                     │
│     └─ Format complete tour object                           │
│                                                               │
│  3️⃣ RETURN                                                  │
│     └─ JSON: {tours: [...], total_found: N}                  │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│              Database Query Flow                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  PostgreSQL Full-Text Search (FTS):                          │
│  • tour_destinations.destination_name                        │
│  • Match user query against stored destination names         │
│  • Return matching tour_ids                                  │
│                                                               │
│  Join Strategy:                                              │
│  tours ←→ tour_destinations                                  │
│  tours ←→ tour_departures                                    │
│  tours ←→ tour_highlight_locations                           │
│  tours ←→ departure_schedules                                │
│         ├→ recurring_schedules                               │
│         └→ specific_departures                               │
│  tours ←→ price_by_packages                                  │
│  tours ←→ price_by_dates                                     │
│  tours ←→ visa_prices                                        │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 🌐 WEB SEARCH INTEGRATION

```
┌──────────────────────────────────────────────────────────────┐
│         🌐 WEB SEARCH SERVICE (External Knowledge)           │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  search_web_information(query, num_results)                  │
│                                                               │
│  1️⃣ Send query to Search API                                │
│     └─ Google/Bing Custom Search API                         │
│                                                               │
│  2️⃣ Process results                                         │
│     ├─ Extract titles, snippets, URLs                        │
│     ├─ Generate summary using LLM                            │
│     └─ Format sources                                        │
│                                                               │
│  3️⃣ Return                                                  │
│     └─ JSON: {summary, sources: [...], total_results}        │
│                                                               │
│  Use Cases:                                                  │
│  • "Hà Nội có gì vui?"                                       │
│  • "Thời tiết Đà Nẵng tháng 12"                              │
│  • "Nên đi du lịch mùa nào?"                                 │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔌 REAL-TIME COMMUNICATION (Socket.IO)

```
┌──────────────────────────────────────────────────────────────┐
│              Socket.IO Architecture                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Server: socketio.AsyncServer (ASGI)                         │
│  • async_mode: 'asgi'                                        │
│  • CORS: allow all origins                                   │
│                                                               │
│  Events:                                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Client → Server                                       │ │
│  │  • connect(chat_id)                                    │ │
│  │  • join_room(chat_id)                                  │ │
│  │  • join_admin_room()                                   │ │
│  │  • disconnect()                                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Server → Client                                       │ │
│  │  • message (to specific chat room)                     │ │
│  │    - message_id, chat_id, content, role, meta_data    │ │
│  │  • admin_notification (to admin room)                  │ │
│  │    - new messages, bookings, payments                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  Room Management:                                            │
│  • Each chat has own room (chat_id)                          │
│  • Admin room for all admins                                 │
│  • Users join specific chat rooms                            │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 CORE TECHNOLOGIES

### Backend Framework

- **FastAPI** - High-performance async web framework
- **Uvicorn** - ASGI server
- **Socket.IO** - Real-time bidirectional communication

### AI/ML

- **AutoGen** - Multi-agent orchestration framework
- **OpenAI API** - LLM (GPT-4/GPT-3.5)
- **LangChain** (potential) - LLM application framework

### Database

- **PostgreSQL** - Main database
- **SQLAlchemy** - ORM
- **Alembic** - Database migration

### External Services

- **Google/Bing Search API** - Web search
- **Facebook Graph API** - Messenger integration
- **Payment Gateways** - VNPay, MoMo

---

## 🎯 KEY FEATURES

### 1. Multi-Agent RAG System

- **4 specialized agents** working together
- **Automatic speaker selection** by GroupChatManager
- **Context-aware** with chat history
- **Tool calling** for database and web search

### 2. Intelligent Routing

- **IntelligentCoordinator** filters simple queries
- **PlannerAgent** handles complex requests
- **RecommendationAgent** provides expert advice

### 3. Real-time Communication

- **WebSocket** for instant messaging
- **Socket.IO rooms** for chat isolation
- **Admin notifications** for monitoring

### 4. Comprehensive Tour Search

- **Full-text search** on destinations
- **Price filtering** (min/max)
- **Date availability** checking
- **Complete tour details** with schedules, prices, highlights

### 5. E-commerce Integration

- **Shopping cart** system
- **Booking management**
- **Payment processing** with webhooks
- **Follow-up automation**

### 6. Multi-channel Support

- **Web application**
- **Facebook Messenger**
- **Email/SMS notifications**

---

## 🚀 DEPLOYMENT

### Local Development

```bash
poetry run uvicorn app:socket_app --reload --host 0.0.0.0 --port 8000
```

### Production (Docker)

```yaml
services:
  - FastAPI app (with Socket.IO)
  - PostgreSQL database
  - Redis (for caching)
  - Nginx (reverse proxy)
```

---

## 📊 DATA MODELS (Main Tables)

```
users
├─ id (UUID)
├─ email
├─ name
└─ created_at

chats
├─ id (UUID)
├─ user_id (FK → users)
├─ session_id (UUID)
├─ title
├─ platform (web/facebook)
└─ external_user_id

messages
├─ id (UUID)
├─ chat_id (FK → chats)
├─ content (TEXT)
├─ role (user/assistant)
├─ meta_data (JSONB) ← Tour search results
└─ created_at

tours
├─ id (UUID)
├─ tour_name
├─ days (INT)
├─ description (TEXT)
├─ highlight (TEXT)
├─ price_type (visa/package/date)
└─ ... (URLs, images)

tour_destinations
├─ id (UUID)
├─ tour_id (FK → tours)
└─ destination_name

departure_schedules
├─ recurring_schedules (weekly/monthly)
│  ├─ recurrence_type
│  ├─ weekdays (ARRAY)
│  ├─ start_date
│  └─ end_date
└─ specific_departures
   ├─ date
   └─ tour_id

bookings
├─ id (UUID)
├─ user_id (FK → users)
├─ tour_id (FK → tours)
├─ status (pending/confirmed/cancelled)
├─ total_price
└─ booking_date
```

---

## 🔐 SECURITY

- **JWT Authentication** for API endpoints
- **Middleware** for auth validation
- **CORS** configuration for web clients
- **Input validation** with Pydantic
- **SQL injection prevention** via ORM
- **Rate limiting** (recommended)

---

## 📈 SCALABILITY CONSIDERATIONS

1. **Agent Pooling** - Reuse agent instances
2. **Caching** - Redis for frequent queries
3. **Database Indexing** - FTS indexes on search fields
4. **Async Processing** - FastAPI async endpoints
5. **Load Balancing** - Multiple app instances
6. **Message Queue** - RabbitMQ/Redis for background tasks

---

## 🔄 FUTURE ENHANCEMENTS

- [ ] Vector database (Pinecone/Weaviate) for semantic search
- [ ] LangChain integration for advanced RAG
- [ ] Voice chat support
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] A/B testing for agent prompts
- [ ] Recommendation system with ML
- [ ] Automated testing suite

---

**Version**: 1.0  
**Last Updated**: December 2025  
**Author**: Travel Chatbot Team
