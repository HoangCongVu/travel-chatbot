# BÁO CÁO ĐỒ ÁN TỐT NGHIỆP

# HỆ THỐNG CHATBOT TƯ VẤN DU LỊCH SỬ DỤNG CÔNG NGHỆ RAG VÀ MULTI-AGENT

---

## CHƯƠNG 1: TỔNG QUAN VỀ ĐỒ ÁN

### 1.1. Giới thiệu đề tài

Trong bối cảnh công nghệ trí tuệ nhân tạo (AI) phát triển mạnh mẽ, đặc biệt là các mô hình ngôn ngữ lớn (Large Language Models - LLMs), việc ứng dụng AI vào lĩnh vực du lịch đang trở thành xu hướng tất yếu. Du lịch là một trong những ngành dịch vụ có tính tương tác cao với khách hàng, đòi hỏi khả năng tư vấn chi tiết, chính xác và kịp thời.

Hiện nay, hầu hết các doanh nghiệp du lịch vẫn dựa vào nhân viên tư vấn trực tiếp hoặc các hệ thống chatbot truyền thống dựa trên rule-based (quy tắc cứng). Các giải pháp này tồn tại nhiều hạn chế:

- **Chatbot rule-based**: Chỉ trả lời được các câu hỏi theo mẫu có sẵn, không linh hoạt
- **Tư vấn thủ công**: Tốn nhiều nhân lực, chi phí cao, không phục vụ 24/7
- **Thông tin không đồng bộ**: Khó cập nhật thông tin thời gian thực về tour, giá cả, thời tiết
- **Trải nghiệm người dùng**: Thời gian chờ đợi lâu, không có tính cá nhân hóa

Để giải quyết những vấn đề trên, đồ án nghiên cứu và xây dựng **"Hệ thống Chatbot Tư vấn Du lịch sử dụng công nghệ RAG (Retrieval-Augmented Generation) và Multi-Agent"**. Hệ thống kết hợp ưu điểm của:

- **RAG**: Tìm kiếm thông tin từ cơ sở dữ liệu tour du lịch và nguồn web
- **Multi-Agent**: 4 AI agents chuyên biệt phối hợp xử lý các tác vụ khác nhau
- **Real-time Communication**: Socket.IO cho trải nghiệm chat mượt mà
- **E-commerce Integration**: Tích hợp đặt tour, giỏ hàng, thanh toán

Hệ thống không chỉ trả lời câu hỏi mà còn **chủ động tư vấn, so sánh các lựa chọn tour, gợi ý phù hợp với nhu cầu** và hỗ trợ **đặt tour trực tiếp** trên nền tảng.

---

### 1.2. Mục tiêu nghiên cứu

#### 1.2.1. Mục tiêu tổng quát

Xây dựng hệ thống chatbot tư vấn du lịch thông minh sử dụng công nghệ RAG và Multi-Agent, có khả năng:

- Tư vấn tour du lịch tự động, chính xác và cá nhân hóa
- Tìm kiếm thông tin thời gian thực từ nhiều nguồn
- Hỗ trợ quy trình đặt tour và thanh toán trực tuyến
- Tích hợp đa kênh (Web, Facebook Messenger)

#### 1.2.2. Mục tiêu cụ thể

##### A. Về mặt nghiên cứu và thiết kế kiến trúc

1. **Nghiên cứu và áp dụng kiến trúc RAG (Retrieval-Augmented Generation)**

   - Tìm hiểu các phương pháp tìm kiếm thông tin (BM25, Ensemble Multi-vector retrieval)
   - Thiết kế pipeline kết hợp tìm kiếm database và sinh ngôn ngữ tự nhiên
   - Xử lý context từ lịch sử chat để tạo câu hỏi có ngữ cảnh

2. **Thiết kế và triển khai hệ thống Multi-Agent**

   - Xây dựng 4 AI agents với vai trò chuyên biệt:
     - **IntelligentCoordinator**: Phân loại và route tin nhắn
     - **PlannerAgent**: Lập kế hoạch và điều phối
     - **UserProxy**: Thực thi function calls
     - **RecommendationAgent**: Tổng hợp và tư vấn
   - Sử dụng AutoGen framework để orchestration các agents
   - Thiết kế cơ chế auto speaker selection và termination

3. **Tích hợp LLM (Large Language Model)**
   - Sử dụng OpenAI GPT-4/GPT-3.5 cho khả năng hiểu ngôn ngữ tự nhiên
   - Thiết kế system prompts tối ưu cho từng agent
   - Xử lý context window và token management

##### B. Về mặt kỹ thuật và triển khai

4. **Xây dựng hệ thống tìm kiếm tour thông minh**

   - Full-text search trên PostgreSQL với tối ưu hóa hiệu năng
   - Tìm kiếm theo đa tiêu chí: điểm đến, giá cả, ngày khởi hành
   - Xử lý lịch khởi hành phức tạp (recurring schedules, specific dates)
   - Làm giàu thông tin tour (departure, destination, prices, highlights)

5. **Phát triển API RESTful và Real-time Communication**

   - Xây dựng API với FastAPI (async/await)
   - Tích hợp Socket.IO cho chat real-time
   - Quản lý rooms và sessions cho multi-user
   - Admin notification system

6. **Thiết kế và triển khai cơ sở dữ liệu**

   - Mô hình hóa dữ liệu cho domain du lịch (tours, schedules, prices, bookings)
   - Sử dụng SQLAlchemy ORM và Alembic cho migration
   - Tối ưu hóa queries và indexing
   - Lưu trữ metadata (tour search results) trong messages

7. **Tích hợp các dịch vụ bên ngoài**
   - Web Search API (Google/Bing) cho thông tin thời gian thực
   - Facebook Messenger API (webhook, send API)
   - Payment Gateway (VNPay, MoMo) với webhook callbacks

##### C. Về mặt chức năng và trải nghiệm người dùng

8. **Phát triển tính năng chatbot thông minh**

   - Xử lý ngôn ngữ tự nhiên tiếng Việt
   - Hiểu context và lịch sử hội thoại
   - Phân biệt intent: tìm tour, hỏi thông tin, chào hỏi, spam
   - Tư vấn chủ động và so sánh các lựa chọn
   - Follow-up tự động

9. **Xây dựng tính năng E-commerce**

   - Quản lý giỏ hàng (carts, cart_items)
   - Đặt tour (bookings) với tracking trạng thái
   - Xử lý thanh toán và webhook
   - Quản lý nhiều loại giá (visa, package, by date)

10. **Hỗ trợ đa kênh và đa nền tảng**
    - Web application
    - Facebook Messenger integration
    - Admin dashboard (monitoring, notifications)
    - Email/SMS notifications

##### D. Về mặt đánh giá và tối ưu

11. **Đánh giá hiệu suất hệ thống**

    - Độ chính xác của câu trả lời (accuracy)
    - Thời gian phản hồi (response time)
    - Số lượng requests xử lý đồng thời
    - Tỷ lệ chuyển đổi (từ chat → booking)

12. **Tối ưu hóa chi phí và hiệu năng**
    - Giảm thiểu số lần gọi LLM API
    - Caching cho các queries phổ biến
    - Token management cho context window
    - Database query optimization

---

### 1.3. Phạm vi nghiên cứu

#### 1.3.1. Phạm vi về mặt chức năng

##### A. Các chức năng ĐƯỢC TRIỂN KHAI trong đồ án

**1. Module Chatbot AI**

- ✅ Hệ thống Multi-Agent (4 agents: Coordinator, Planner, UserProxy, Recommendation)
- ✅ RAG pipeline với database search và web search
- ✅ Xử lý ngôn ngữ tự nhiên tiếng Việt
- ✅ Context-aware conversation (lịch sử 10 tin nhắn gần nhất)
- ✅ Tour context retention (ghi nhớ tour đã tìm trong conversation)
- ✅ Phân loại intent và routing tự động
- ✅ Tư vấn và so sánh tour
- ✅ Real-time chat với Socket.IO

**2. Module Quản lý Tour**

- ✅ CRUD tours với đầy đủ thông tin (tên, mô tả, lịch trình, highlight)
- ✅ Quản lý điểm khởi hành (departures) và điểm đến (destinations)
- ✅ Quản lý lịch khởi hành:
  - Recurring schedules (theo tuần/tháng)
  - Specific departure dates
- ✅ Quản lý giá linh hoạt:
  - Giá theo visa (visa_prices)
  - Giá theo gói (price_by_packages)
  - Giá theo ngày (price_by_dates)
- ✅ Quản lý điểm nhấn/địa điểm nổi bật (highlight locations)
- ✅ Quản lý loại tour (tour types)

**3. Module Tìm kiếm Tour**

- ✅ Full-text search theo điểm đến
- ✅ Tìm kiếm theo khoảng giá (min/max price)
- ✅ Tìm kiếm theo ngày khởi hành cụ thể
- ✅ Tìm kiếm theo tháng
- ✅ Tìm kiếm kết hợp (điểm khởi hành + điểm đến)
- ✅ Enrichment thông tin tour (schedules, prices, highlights)

**4. Module Tìm kiếm Web**

- ✅ Web search API integration (Google/Bing)
- ✅ Tìm kiếm thông tin thời gian thực
- ✅ Tổng hợp và format kết quả tìm kiếm
- ✅ Trích xuất sources (title, snippet, URL)

**5. Module Quản lý Người dùng**

- ✅ Đăng ký, đăng nhập user
- ✅ Quản lý thông tin user (name, email)
- ✅ Phân quyền (admin/user)
- ✅ Session management

**6. Module Quản lý Chat**

- ✅ Tạo chat sessions (web, Facebook)
- ✅ Lưu trữ lịch sử messages với role (user/assistant)
- ✅ Metadata trong messages (lưu tour search results)
- ✅ Multi-platform support (platform, external_user_id)
- ✅ Real-time updates qua Socket.IO
- ✅ Admin monitoring (admin room, notifications)

**7. Module E-commerce**

- ✅ Giỏ hàng (carts, cart_items)
- ✅ Đặt tour (bookings) với trạng thái (pending/confirmed/cancelled)
- ✅ Quản lý thanh toán (payments)
- ✅ Payment webhook integration (VNPay, MoMo)
- ✅ Tính toán tổng giá dựa trên loại giá tour

**8. Module Facebook Messenger**

- ✅ Webhook verification và message handling
- ✅ Send API integration
- ✅ User mapping (external_user_id → chat)
- ✅ Bi-directional messaging

**9. Module File Management**

- ✅ Upload files (images, documents)
- ✅ Storage management
- ✅ File metadata tracking

**10. Module Follow-up**

- ✅ Cấu hình follow-up settings
- ✅ Templates cho tin nhắn follow-up
- ✅ Auto-scheduling (background job)

##### B. Các chức năng KHÔNG TRIỂN KHAI (ngoài phạm vi)

**1. AI/ML nâng cao**

- ❌ Vector database (Pinecone, Weaviate, ChromaDB) cho semantic search
- ❌ Fine-tuning mô hình LLM riêng cho domain du lịch Việt Nam
- ❌ Sentiment analysis và emotion detection
- ❌ Recommendation system dựa trên Machine Learning (collaborative filtering)
- ❌ Speech-to-text và text-to-speech cho voice chat
- ❌ Image recognition cho ảnh điểm đến

**2. Tính năng nâng cao**

- ❌ Multi-language support (Anh, Trung, Nhật, Hàn)
- ❌ Video call tư vấn trực tiếp
- ❌ AR/VR preview tour
- ❌ Gamification (điểm thưởng, loyalty program)
- ❌ Social features (đánh giá, review, sharing)
- ❌ Blog/Content management system

**3. Analytics và Business Intelligence**

- ❌ Dashboard analytics nâng cao
- ❌ A/B testing framework
- ❌ Customer journey tracking chi tiết
- ❌ Predictive analytics (dự đoán xu hướng đặt tour)
- ❌ Heat maps và user behavior analysis

**4. Integration nâng cao**

- ❌ Zalo, Telegram, WhatsApp integration
- ❌ Google Calendar/Apple Calendar sync
- ❌ Flight/Hotel booking APIs
- ❌ Weather API integration chi tiết
- ❌ Map visualization (Google Maps embed)
- ❌ CRM system integration (Salesforce, HubSpot)

#### 1.3.2. Phạm vi về mặt kỹ thuật

##### A. Công nghệ SỬ DỤNG

**Backend**

- ✅ Python 3.11+
- ✅ FastAPI (async web framework)
- ✅ Uvicorn (ASGI server)
- ✅ Socket.IO (real-time communication)
- ✅ SQLAlchemy (ORM)
- ✅ Alembic (database migration)
- ✅ Pydantic (data validation)

**AI/ML**

- ✅ AutoGen (multi-agent framework)
- ✅ OpenAI API (GPT-4, GPT-3.5-turbo)
- ✅ LangChain (utilities, nếu có)

**Database**

- ✅ PostgreSQL (main database)
- ✅ Full-text search (PostgreSQL FTS)

**External APIs**

- ✅ OpenAI API
- ✅ Google/Bing Search API
- ✅ Facebook Graph API (Messenger)
- ✅ VNPay/MoMo Payment API

**DevOps**

- ✅ Poetry (dependency management)
- ✅ Docker & Docker Compose (containerization)
- ✅ Git (version control)
- ✅ Environment variables (.env)

##### B. Công nghệ KHÔNG SỬ DỤNG (ngoài phạm vi)

**Advanced AI**

- ❌ Vector databases (Pinecone, Weaviate, Milvus)
- ❌ Embedding models training
- ❌ Custom LLM fine-tuning
- ❌ TensorFlow/PyTorch cho custom models

**Infrastructure**

- ❌ Kubernetes orchestration
- ❌ Microservices architecture
- ❌ Message queues (RabbitMQ, Kafka) cho scale lớn
- ❌ Redis cluster cho distributed caching
- ❌ Elasticsearch cho advanced search
- ❌ CI/CD pipelines (Jenkins, GitHub Actions)
- ❌ Monitoring tools (Prometheus, Grafana)
- ❌ Load testing và stress testing tools

**Frontend** (nếu có)

- ❌ React/Vue/Angular SPA
- ❌ Mobile apps (iOS, Android)
- ❌ Progressive Web App (PWA)

#### 1.3.3. Phạm vi về mặt dữ liệu

##### A. Dữ liệu ĐƯỢC XỬ LÝ

**1. Tour data**

- ✅ Thông tin cơ bản: tên, mô tả, số ngày, highlight
- ✅ Điểm khởi hành và điểm đến (text-based)
- ✅ Lịch khởi hành (recurring + specific dates)
- ✅ Giá tour (3 loại: visa/package/date)
- ✅ Địa điểm nổi bật
- ✅ URL ảnh và lịch trình
- ✅ Thông tin khuyến mãi

**2. User & Chat data**

- ✅ Thông tin user cơ bản (name, email)
- ✅ Chat sessions (web, Facebook)
- ✅ Messages với role và metadata
- ✅ Lịch sử chat (recent 10 messages)
- ✅ Tour context trong conversation

**3. Booking & Payment data**

- ✅ Booking information (user, tour, dates, passengers)
- ✅ Cart data (items, quantities)
- ✅ Payment transactions
- ✅ Webhook payloads

**4. External data**

- ✅ Web search results (real-time)
- ✅ Facebook user profiles (basic info)

##### B. Dữ liệu KHÔNG XỬ LÝ (ngoài phạm vi)

- ❌ Geolocation data (coordinates, maps)
- ❌ User behavior tracking chi tiết
- ❌ Image/video data processing
- ❌ Flight/hotel availability data
- ❌ Real-time weather data
- ❌ Social media sentiment data
- ❌ User preferences và behavioral patterns (ML-based)

#### 1.3.4. Phạm vi về mặt triển khai

##### A. Môi trường triển khai

**Development**

- ✅ Local development với Poetry
- ✅ Docker Compose cho local testing
- ✅ Hot reload với Uvicorn

**Production** (Mục tiêu)

- ✅ Docker containers
- ✅ PostgreSQL production database
- ⚠️ Single server deployment (không phải distributed system)

##### B. Scale và Performance

**Target metrics**

- Số user đồng thời: **50-100 users**
- Response time: **< 5 seconds** cho chatbot reply
- Database size: **< 10,000 tours**
- Message throughput: **< 100 messages/minute**
- Uptime: **Không yêu cầu 99.9% (không critical production)**

**Không hỗ trợ**

- ❌ High availability (multi-region, failover)
- ❌ Horizontal scaling với load balancer
- ❌ Auto-scaling dựa trên traffic
- ❌ CDN cho static assets
- ❌ Database replication và sharding

#### 1.3.5. Phạm vi về mặt người dùng

##### A. Đối tượng người dùng MỤC TIÊU

1. **Khách hàng tiềm năng**

   - Người Việt muốn tìm tour du lịch
   - Độ tuổi: 18-50
   - Sử dụng Web hoặc Facebook Messenger
   - Có nhu cầu tư vấn tour nhanh chóng

2. **Admin/Staff**
   - Quản lý tours, bookings
   - Theo dõi chats và messages
   - Xử lý payments

##### B. Không hỗ trợ

- ❌ Khách hàng quốc tế (chỉ tiếng Việt)
- ❌ Đối tác B2B (travel agencies)
- ❌ Tour operators (complex workflows)

#### 1.3.6. Phạm vi về mặt domain nghiệp vụ

##### A. Loại hình du lịch ĐƯỢC HỖ TRỢ

- ✅ Tour du lịch trọn gói (package tours)
- ✅ Tour trong nước (Việt Nam)
- ✅ Tour nước ngoài
- ✅ Tour ngắn ngày (1-3 ngày)
- ✅ Tour dài ngày (> 3 ngày)

##### B. Loại hình KHÔNG HỖ TRỢ

- ❌ Tour tự túc (self-guided)
- ❌ Đặt vé máy bay riêng lẻ
- ❌ Đặt khách sạn riêng lẻ
- ❌ Thuê xe riêng
- ❌ Tour du thuyền, cruise
- ❌ Tour adventure chuyên sâu (leo núi, lặn biển)

---

### 1.4. Ý nghĩa khoa học và thực tiễn

#### 1.4.1. Ý nghĩa khoa học

1. **Nghiên cứu kiến trúc Multi-Agent cho chatbot domain-specific**

   - Đề xuất mô hình 4-agent với vai trò rõ ràng
   - So sánh với các kiến trúc single-agent và 2-agent
   - Đánh giá hiệu quả của auto speaker selection

2. **Ứng dụng RAG trong lĩnh vực du lịch**

   - Kết hợp database search và web search
   - Xử lý context và lịch sử hội thoại
   - Tối ưu hóa prompt engineering cho từng agent

3. **Đóng góp về mặt kỹ thuật**
   - Tích hợp LLM với hệ thống legacy (database, APIs)
   - Real-time communication với Socket.IO trong AI chatbot
   - Metadata management cho search results

#### 1.4.2. Ý nghĩa thực tiễn

1. **Cho doanh nghiệp du lịch**

   - Giảm chi phí nhân sự tư vấn (ước tính 40-60%)
   - Phục vụ khách hàng 24/7 không gián đoạn
   - Tăng tỷ lệ chuyển đổi từ chat → booking
   - Thu thập dữ liệu insight từ chat logs

2. **Cho khách hàng**

   - Nhận tư vấn tức thì, không cần chờ đợi
   - So sánh nhiều lựa chọn tour một cách dễ dàng
   - Đặt tour trực tiếp qua chat (seamless experience)
   - Trải nghiệm cá nhân hóa dựa trên lịch sử chat

3. **Cho cộng đồng nghiên cứu**
   - Mã nguồn mở (nếu có) cho cộng đồng tham khảo
   - Tài liệu hóa kiến trúc Multi-Agent rõ ràng
   - Case study thực tế về RAG trong e-commerce

---

### 1.5. Đối tượng và phạm vi áp dụng

#### 1.5.1. Đối tượng áp dụng

- Các công ty du lịch vừa và nhỏ (SMEs)
- Travel agents muốn số hóa quy trình tư vấn
- Startups trong lĩnh vực travel-tech
- Các trường đại học nghiên cứu về AI/NLP

#### 1.5.2. Phạm vi áp dụng

- Thị trường Việt Nam (tiếng Việt)
- Quy mô: 100-10,000 tours trong database
- User base: < 1,000 active users

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT

### 2.1. Tổng quan về Chatbot và hệ thống hội thoại

#### 2.1.1. Định nghĩa Chatbot

Chatbot (chat robot) là một chương trình máy tính được thiết kế để mô phỏng cuộc trò chuyện với người dùng thông qua giao diện văn bản hoặc giọng nói. Chatbot sử dụng các kỹ thuật xử lý ngôn ngữ tự nhiên (Natural Language Processing - NLP) và trí tuệ nhân tạo (AI) để hiểu và phản hồi các yêu cầu của người dùng một cách tự động.

#### 2.1.2. Phân loại Chatbot

**A. Theo phương pháp xử lý**

1. **Rule-based Chatbot (Dựa trên quy tắc)**

   - Hoạt động dựa trên tập hợp các quy tắc được định nghĩa trước
   - Sử dụng pattern matching và decision trees
   - **Ưu điểm**: Dễ xây dựng, dễ kiểm soát, chi phí thấp
   - **Nhược điểm**: Không linh hoạt, chỉ trả lời được các câu hỏi có mẫu
   - **Ví dụ**: Chatbot hỗ trợ khách hàng với menu lựa chọn cố định

2. **AI-powered Chatbot (Dựa trên AI/ML)**

   - Sử dụng Machine Learning và Deep Learning
   - Có khả năng học từ dữ liệu và cải thiện theo thời gian
   - **Ưu điểm**: Linh hoạt, hiểu ngữ cảnh, xử lý câu hỏi phức tạp
   - **Nhược điểm**: Chi phí cao, cần nhiều dữ liệu training, khó debug
   - **Ví dụ**: ChatGPT, Google Assistant, Siri

3. **Hybrid Chatbot (Kết hợp)**
   - Kết hợp rule-based và AI-powered
   - Sử dụng rules cho các tác vụ đơn giản, AI cho tác vụ phức tạp
   - **Ưu điểm**: Cân bằng giữa kiểm soát và linh hoạt
   - **Nhược điểm**: Phức tạp trong thiết kế và triển khai

**B. Theo chức năng**

1. **Task-oriented (Conversational) Chatbot**

   - Tập trung vào một nhiệm vụ cụ thể
   - Ví dụ: Đặt vé máy bay, đặt phòng khách sạn

2. **Open-domain Chatbot**
   - Có thể trò chuyện về nhiều chủ đề
   - Ví dụ: ChatGPT, Claude

#### 2.1.3. Kiến trúc cơ bản của Chatbot

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Natural Language Understanding     │
│  (NLU)                              │
│  • Tokenization                     │
│  • Intent Classification            │
│  • Entity Recognition               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Dialogue Management                │
│  • Context Tracking                 │
│  • State Management                 │
│  • Action Selection                 │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Natural Language Generation        │
│  (NLG)                              │
│  • Response Generation              │
│  • Text Formatting                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────┐
│   Response  │
└─────────────┘
```

---

### 2.2. Large Language Models (LLMs)

#### 2.2.1. Giới thiệu về LLM

Large Language Models (LLMs) là các mô hình ngôn ngữ lớn được huấn luyện trên lượng dữ liệu khổng lồ (hàng tỷ đến hàng nghìn tỷ từ) từ internet, sách, bài báo, code, v.v. LLMs có khả năng:

- Hiểu và sinh ngôn ngữ tự nhiên
- Thực hiện reasoning và suy luận logic
- Trả lời câu hỏi dựa trên kiến thức đã học
- Tạo nội dung sáng tạo (văn bản, code, etc.)

#### 2.2.2. Kiến trúc Transformer

LLMs hiện đại đều dựa trên kiến trúc **Transformer** (Vaswani et al., 2017):

**Các thành phần chính:**

1. **Self-Attention Mechanism**

   - Cho phép mô hình "chú ý" đến các phần khác nhau của input
   - Tính toán mối quan hệ giữa các tokens
   - Formula: `Attention(Q, K, V) = softmax(QK^T / √d_k)V`

2. **Multi-Head Attention**

   - Nhiều attention heads song song
   - Mỗi head học các patterns khác nhau

3. **Feed-Forward Networks**

   - Xử lý thông tin từ attention layers
   - Thường có 2 fully connected layers

4. **Positional Encoding**
   - Mã hóa vị trí của tokens trong sequence
   - Giúp mô hình hiểu thứ tự từ

#### 2.2.3. Các mô hình LLM phổ biến

| Model         | Organization | Parameters | Release Date | Đặc điểm                  |
| ------------- | ------------ | ---------- | ------------ | ------------------------- |
| GPT-3         | OpenAI       | 175B       | 2020         | Few-shot learning tốt     |
| GPT-3.5-turbo | OpenAI       | ~175B      | 2022         | Tối ưu cho chat, giá rẻ   |
| GPT-4         | OpenAI       | Unknown    | 2023         | Multimodal, reasoning tốt |
| Claude 3      | Anthropic    | Unknown    | 2024         | Context window 200K       |
| LLaMA 2       | Meta         | 7B-70B     | 2023         | Open-source               |
| Gemini        | Google       | Unknown    | 2023         | Multimodal native         |

#### 2.2.4. Prompting và In-Context Learning

**A. Prompt Engineering**

Prompt là đoạn text đầu vào để hướng dẫn LLM thực hiện tác vụ.

**Các kỹ thuật prompting:**

1. **Zero-shot Prompting**

   ```
   User: "Phân loại câu này: 'Tôi muốn đi Hà Nội'"
   LLM: "Đây là câu yêu cầu về du lịch"
   ```

2. **Few-shot Prompting**

   ```
   User: "
   Ví dụ 1: 'Xin chào' → Greeting
   Ví dụ 2: 'Tour Đà Nẵng' → Tour Query

   Phân loại: 'Tìm tour Hạ Long'
   "
   LLM: "Tour Query"
   ```

3. **Chain-of-Thought (CoT) Prompting**

   ```
   User: "Hãy suy nghĩ từng bước để trả lời:
   User muốn đi du lịch 3 ngày ở miền Bắc vào tháng 12.
   Nên gợi ý tour nào?"

   LLM: "
   Bước 1: Xác định yêu cầu - 3 ngày, miền Bắc, tháng 12
   Bước 2: Tháng 12 miền Bắc trời lạnh, phù hợp Sapa, Hà Nội
   Bước 3: Gợi ý Tour Sapa 3N2Đ hoặc Tour Hà Nội - Hạ Long 3N2Đ
   "
   ```

**B. System Message vs User Message**

- **System Message**: Định nghĩa vai trò và hành vi của LLM
- **User Message**: Input từ người dùng
- **Assistant Message**: Response từ LLM

#### 2.2.5. Hạn chế của LLMs

1. **Hallucination** (Ảo giác)

   - LLM có thể tạo ra thông tin sai lệch, không có trong dữ liệu training
   - Đặc biệt nghiêm trọng với thông tin cụ thể (số liệu, ngày tháng, giá cả)

2. **Knowledge Cutoff**

   - LLM chỉ biết thông tin đến thời điểm training
   - Không có thông tin real-time

3. **Context Window Limitation**

   - Giới hạn số tokens có thể xử lý (4K - 200K tokens)
   - Không thể xử lý toàn bộ database lớn

4. **Chi phí cao**
   - API calls tốn kém ($0.01 - $0.06 per 1K tokens)
   - Latency (độ trễ) 2-10 giây

→ **Giải pháp**: Sử dụng **RAG (Retrieval-Augmented Generation)**

---

### 2.3. Retrieval-Augmented Generation (RAG)

#### 2.3.1. Định nghĩa và động lực

**RAG** (Lewis et al., 2020) là kỹ thuật kết hợp **retrieval (tìm kiếm)** và **generation (sinh văn bản)** để cải thiện chất lượng câu trả lời của LLM.

**Động lực phát triển RAG:**

- LLM có kiến thức chung nhưng thiếu thông tin domain-specific
- Hallucination gây ra thông tin sai lệch
- Cần cập nhật thông tin real-time mà không cần retrain model
- Chi phí fine-tuning cao và phức tạp

**Ý tưởng chính:**

> Thay vì yêu cầu LLM trả lời dựa trên kiến thức đã học, RAG cung cấp thông tin liên quan (retrieved documents) để LLM dựa vào đó sinh câu trả lời.

#### 2.3.2. Kiến trúc RAG

```
┌──────────────┐
│ User Query   │
└──────┬───────┘
       │
       ▼
┌────────────────────────────────────┐
│  RETRIEVAL PHASE                   │
├────────────────────────────────────┤
│  1. Query Processing               │
│     • Normalize query              │
│     • Extract keywords             │
│     • Generate embeddings          │
│                                    │
│  2. Document Retrieval             │
│     • Search in knowledge base     │
│     • Vector similarity search     │
│     • BM25 / TF-IDF ranking        │
│                                    │
│  3. Re-ranking (optional)          │
│     • Score documents              │
│     • Select top-k relevant docs   │
└──────────┬─────────────────────────┘
           │
           ▼
    ┌─────────────┐
    │  Retrieved  │
    │  Documents  │
    └──────┬──────┘
           │
           ▼
┌────────────────────────────────────┐
│  AUGMENTATION PHASE                │
├────────────────────────────────────┤
│  • Combine query + documents       │
│  • Format context for LLM          │
│  • Build prompt                    │
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  GENERATION PHASE                  │
├────────────────────────────────────┤
│  LLM generates answer based on:    │
│  • User query                      │
│  • Retrieved documents             │
│  • System instructions             │
└──────────┬─────────────────────────┘
           │
           ▼
    ┌─────────────┐
    │   Answer    │
    └─────────────┘
```

#### 2.3.3. Các phương pháp Retrieval

**A. Keyword-based Search**

1. **BM25 (Best Matching 25)**

   - Cải tiến của TF-IDF
   - Tính điểm dựa trên:
     - Term frequency (tần suất từ)
     - Inverse document frequency
     - Document length normalization

   Formula:

   ```
   score(D, Q) = Σ IDF(q_i) · (f(q_i, D) · (k_1 + 1)) / (f(q_i, D) + k_1 · (1 - b + b · |D| / avgdl))
   ```

2. **TF-IDF (Term Frequency-Inverse Document Frequency)**
   - TF: Số lần từ xuất hiện trong document
   - IDF: Đánh giá độ hiếm của từ trong corpus

**B. Semantic Search (Vector-based)**

1. **Dense Retrieval**

   - Sử dụng embeddings (vectors) để biểu diễn query và documents
   - Tìm kiếm dựa trên cosine similarity
   - Models: BERT, sentence-transformers, OpenAI embeddings

2. **Hybrid Search**
   - Kết hợp keyword search và semantic search
   - **Ensemble**: Kết hợp điểm số từ nhiều phương pháp
   - Cải thiện cả precision và recall

**C. Multi-vector Retrieval**

Models như **BGE-M3** (BAAI) tạo nhiều vectors cho mỗi document:

- Sparse vector (từ khóa)
- Dense vector (semantic)
- Multi-vector (token-level representations)

#### 2.3.4. Vector Databases

**Vector Database** là hệ quản trị cơ sở dữ liệu được tối ưu cho lưu trữ và tìm kiếm vectors (embeddings).

**Các vector database phổ biến:**

- **Pinecone**: Managed service, scalable
- **Weaviate**: Open-source, GraphQL support
- **ChromaDB**: Lightweight, Python-native
- **Milvus**: High performance, distributed
- **FAISS**: Facebook AI, library (không phải full DB)

**So sánh với PostgreSQL:**

- PostgreSQL: Tốt cho structured data, keyword search
- Vector DB: Tối ưu cho similarity search, embeddings
- Hybrid: PostgreSQL + pgvector extension

#### 2.3.5. Context Window và Chunking

**A. Context Window**

- Giới hạn số tokens LLM có thể xử lý trong 1 request
- GPT-3.5-turbo: 4K - 16K tokens
- GPT-4: 8K - 128K tokens
- Claude 3: 200K tokens

**B. Chunking Strategy**

Chia documents lớn thành chunks nhỏ để:

- Fit vào context window
- Cải thiện độ chính xác retrieval
- Giảm noise

**Các phương pháp chunking:**

1. **Fixed-size chunking**: Chia theo số ký tự/tokens cố định
2. **Semantic chunking**: Chia theo đoạn văn, câu
3. **Sliding window**: Chunks overlap để giữ context
4. **Hierarchical chunking**: Chunks lồng nhau (paragraph → sentence)

#### 2.3.6. Ưu và nhược điểm của RAG

**Ưu điểm:**

- ✅ Giảm hallucination (dựa trên dữ liệu thực)
- ✅ Cập nhật thông tin dễ dàng (chỉ cần update database)
- ✅ Domain-specific knowledge (không cần fine-tune LLM)
- ✅ Truy xuất nguồn (trích dẫn documents)
- ✅ Chi phí thấp hơn fine-tuning

**Nhược điểm:**

- ❌ Phụ thuộc vào chất lượng retrieval
- ❌ Latency tăng (do retrieval step)
- ❌ Context window limitation (không thể retrieve quá nhiều)
- ❌ Cần infrastructure cho search (vector DB, indexing)

---

### 2.4. Multi-Agent Systems

#### 2.4.1. Định nghĩa Agent và Multi-Agent System

**Agent (AI Agent):**

- Là một thực thể tự động có khả năng:
  - Perceive (cảm nhận) môi trường
  - Reason (suy luận) về tình huống
  - Act (hành động) để đạt mục tiêu
- Trong context của LLM: Agent = LLM + Tools + Memory + Planning

**Multi-Agent System (MAS):**

- Hệ thống gồm nhiều agents tương tác với nhau
- Mỗi agent có vai trò và năng lực riêng
- Phối hợp để giải quyết các vấn đề phức tạp

#### 2.4.2. Kiến trúc Multi-Agent

```
┌─────────────────────────────────────────────┐
│         Multi-Agent System                  │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────┐    ┌──────────┐              │
│  │ Agent 1  │◄──►│ Agent 2  │              │
│  │ (Role A) │    │ (Role B) │              │
│  └────┬─────┘    └────┬─────┘              │
│       │               │                     │
│       │    ┌──────────▼─────┐               │
│       └───►│   Orchestrator │               │
│            │   (Coordinator) │               │
│            └──────────┬──────┘               │
│                       │                     │
│            ┌──────────▼─────┐               │
│            │    Agent 3     │               │
│            │   (Role C)     │               │
│            └────────────────┘               │
│                                             │
│  Shared Resources:                          │
│  • Message Queue                            │
│  • Shared Memory                            │
│  • Tools/Functions                          │
└─────────────────────────────────────────────┘
```

#### 2.4.3. Các mô hình tương tác Agent

**A. Sequential (Tuần tự)**

```
Agent A → Agent B → Agent C → Result
```

- Agents thực thi theo thứ tự cố định
- Ví dụ: Pipeline xử lý dữ liệu

**B. Hierarchical (Phân cấp)**

```
       Manager Agent
      /       |       \
Agent 1    Agent 2    Agent 3
```

- Manager agent điều phối các worker agents
- Ví dụ: Boss-worker pattern

**C. Collaborative (Cộng tác)**

```
Agent A ←→ Agent B ←→ Agent C
   ↕         ↕         ↕
      Shared Context
```

- Agents trao đổi thông tin tự do
- GroupChat, debate, consensus

**D. Competitive (Cạnh tranh)**

```
Agent A →]
Agent B →] → Selector → Best Result
Agent C →]
```

- Nhiều agents đề xuất giải pháp
- Chọn kết quả tốt nhất

#### 2.4.4. AutoGen Framework

**AutoGen** (Microsoft Research, 2023) là framework cho multi-agent conversation.

**Các thành phần chính:**

1. **AssistantAgent**

   - Agent dựa trên LLM
   - Có thể gọi functions/tools
   - Có system message định nghĩa vai trò

2. **UserProxyAgent**

   - Đại diện cho user
   - Thực thi code và function calls
   - Có thể yêu cầu human input

3. **GroupChat**

   - Quản lý nhiều agents
   - Speaker selection strategy:
     - `auto`: LLM chọn speaker tiếp theo
     - `round_robin`: Lần lượt
     - `random`: Ngẫu nhiên
     - `manual`: User chọn

4. **GroupChatManager**
   - Điều phối GroupChat
   - Quản lý termination conditions
   - Theo dõi message history

**Ví dụ cấu trúc AutoGen:**

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Define agents
agent1 = AssistantAgent(
    name="Researcher",
    system_message="You are a research expert",
    llm_config={"model": "gpt-4"}
)

agent2 = AssistantAgent(
    name="Writer",
    system_message="You are a writer",
    llm_config={"model": "gpt-4"}
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding"}
)

# Create GroupChat
groupchat = GroupChat(
    agents=[agent1, agent2, user_proxy],
    messages=[],
    max_round=10
)

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"model": "gpt-4"}
)

# Start conversation
user_proxy.initiate_chat(manager, message="Research about AI")
```

#### 2.4.5. Function Calling trong Multi-Agent

**Function Calling** cho phép LLM gọi các hàm external để:

- Truy xuất dữ liệu từ database
- Gọi APIs
- Thực thi code
- Tương tác với tools

**Flow:**

```
1. LLM quyết định cần gọi function
2. LLM tạo function call với parameters
3. UserProxy thực thi function
4. Kết quả được trả về cho LLM
5. LLM tổng hợp kết quả và trả lời user
```

**Ví dụ Function Schema:**

```json
{
  "name": "search_tour",
  "description": "Search for tours by destination",
  "parameters": {
    "type": "object",
    "properties": {
      "destination": {
        "type": "string",
        "description": "Destination name"
      },
      "min_price": {
        "type": "number",
        "description": "Minimum price"
      }
    },
    "required": ["destination"]
  }
}
```

#### 2.4.6. Ưu điểm của Multi-Agent

1. **Specialization** (Chuyên môn hóa)

   - Mỗi agent tập trung vào một tác vụ cụ thể
   - Prompt engineering đơn giản hơn
   - Hiệu quả cao hơn single-agent generalist

2. **Modularity** (Tính module)

   - Dễ bảo trì và nâng cấp từng agent
   - Có thể thay đổi một agent mà không ảnh hưởng toàn hệ thống

3. **Scalability** (Khả năng mở rộng)

   - Thêm agents mới cho chức năng mới
   - Phân tải công việc

4. **Robustness** (Độ ổn định)

   - Một agent lỗi không làm sập toàn hệ thống
   - Agents có thể kiểm tra lẫn nhau (verification)

5. **Complex Problem Solving**
   - Chia nhỏ vấn đề phức tạp thành các subtasks
   - Phối hợp giải quyết từng phần

---

### 2.5. Natural Language Processing (NLP) cho tiếng Việt

#### 2.5.1. Đặc thủ của tiếng Việt

1. **Không có khoảng trắng giữa syllables trong từ ghép**

   - "Hà Nội" vs "ha noi" (2 từ riêng biệt)
   - Cần word segmentation

2. **Dấu thanh (tones)**

   - 6 thanh: ngang, huyền, sắc, hỏi, ngã, nặng
   - Ảnh hưởng nghĩa: "ma", "mà", "má", "mả", "mã", "mạ"

3. **Từ đồng âm khác nghĩa**

   - "không" (空 - trống) vs "không" (không phải)

4. **Ngữ cảnh quan trọng**
   - "Đi Hà Nội" vs "Hà Nội đi"
   - Thứ tự từ linh hoạt hơn tiếng Anh

#### 2.5.2. Tokenization cho tiếng Việt

**Word Segmentation:**

- **VnCoreNLP**: Java-based, accuracy cao
- **pyvi**: Python, dựa trên dictionary
- **underthesea**: Python native, đơn giản

**Subword Tokenization (cho LLMs):**

- **BPE (Byte Pair Encoding)**: GPT models
- **WordPiece**: BERT
- **SentencePiece**: Universal, language-agnostic

#### 2.5.3. Intent Classification

**Intent** là ý định của user trong câu nói.

**Ví dụ:**

- "Tìm tour Đà Nẵng" → Intent: `search_tour`
- "Giá bao nhiêu?" → Intent: `ask_price`
- "Xin chào" → Intent: `greeting`

**Phương pháp:**

1. **Rule-based**: Pattern matching, regex
2. **ML-based**: SVM, Random Forest với TF-IDF features
3. **Deep Learning**: CNN, RNN, BERT for classification
4. **LLM-based**: Few-shot learning với GPT-4

#### 2.5.4. Named Entity Recognition (NER)

**NER** là task nhận diện các entities (thực thể) trong text.

**Entities trong domain du lịch:**

- `DESTINATION`: Hà Nội, Đà Nẵng, Phú Quốc
- `DEPARTURE`: TP.HCM, Hà Nội
- `DATE`: ngày mai, 15/12, tháng 1
- `DURATION`: 3 ngày, 1 tuần
- `PRICE`: 5 triệu, 10tr

**Models cho tiếng Việt:**

- **PhoBERT**: Pre-trained BERT cho tiếng Việt
- **viBERT**: Vietnamese BERT
- **XLM-RoBERTa**: Multilingual

---

### 2.6. Công nghệ Web và API

#### 2.6.1. RESTful API

**REST (Representational State Transfer)** là architectural style cho web services.

**Nguyên tắc:**

- **Stateless**: Mỗi request độc lập
- **Resource-based**: URL đại diện cho resources
- **HTTP methods**: GET, POST, PUT, DELETE
- **JSON format**: Định dạng dữ liệu phổ biến

**Ví dụ endpoints:**

```
GET    /api/tours          # Lấy danh sách tours
GET    /api/tours/{id}     # Lấy 1 tour
POST   /api/tours          # Tạo tour mới
PUT    /api/tours/{id}     # Cập nhật tour
DELETE /api/tours/{id}     # Xóa tour
```

#### 2.6.2. FastAPI Framework

**FastAPI** là modern, high-performance web framework cho Python.

**Đặc điểm:**

- **Async/await support**: Xử lý concurrent requests
- **Automatic API docs**: Swagger UI, ReDoc
- **Type hints**: Pydantic validation
- **Fast**: Performance tương đương Node.js, Go

**Ví dụ:**

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Tour(BaseModel):
    name: str
    price: float
    days: int

@app.post("/tours")
async def create_tour(tour: Tour):
    # Save to database
    return {"tour_id": "123", "status": "created"}
```

#### 2.6.3. WebSocket và Socket.IO

**WebSocket** là giao thức full-duplex cho real-time communication.

**So sánh với HTTP:**

- **HTTP**: Request-response, one-way
- **WebSocket**: Bi-directional, persistent connection

**Socket.IO** là library xây dựng trên WebSocket với:

- Automatic reconnection
- Broadcasting
- Rooms và namespaces
- Fallback to polling nếu WebSocket không khả dụng

**Use cases:**

- Chat applications
- Real-time notifications
- Live updates
- Collaborative editing

#### 2.6.4. Database và ORM

**A. PostgreSQL**

PostgreSQL là RDBMS (Relational Database Management System) mạnh mẽ với:

- ACID transactions
- JSON/JSONB support
- Full-text search
- Extensibility (pgvector, etc.)

**B. SQLAlchemy ORM**

SQLAlchemy là ORM (Object-Relational Mapping) cho Python:

- Map Python classes → Database tables
- Query API thay vì raw SQL
- Relationship management
- Migration với Alembic

**Ví dụ:**

```python
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Tour(Base):
    __tablename__ = "tours"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
```

---

### 2.7. Tổng hợp: Kết hợp các công nghệ trong Travel Chatbot

Hệ thống Travel Chatbot kết hợp tất cả các công nghệ trên:

```
┌──────────────────────────────────────────────────────┐
│              TRAVEL CHATBOT SYSTEM                   │
├──────────────────────────────────────────────────────┤
│                                                       │
│  🤖 Multi-Agent System (AutoGen)                     │
│     ├─ Coordinator Agent                             │
│     ├─ Planner Agent ──────┐                         │
│     ├─ UserProxy Agent     │                         │
│     └─ Recommendation Agent│                         │
│                             │                         │
│  🔍 RAG Pipeline ◄──────────┘                        │
│     ├─ Database Search (PostgreSQL FTS)              │
│     ├─ Web Search (Google API)                       │
│     └─ Context Augmentation                          │
│                                                       │
│  🧠 LLM (OpenAI GPT-4)                               │
│     └─ Natural Language Understanding & Generation   │
│                                                       │
│  🌐 API Layer (FastAPI)                              │
│     ├─ RESTful endpoints                             │
│     └─ Socket.IO for real-time                       │
│                                                       │
│  💾 Data Layer                                       │
│     ├─ PostgreSQL (tours, users, chats)              │
│     └─ SQLAlchemy ORM                                │
│                                                       │
└──────────────────────────────────────────────────────┘
```

**Luồng xử lý tích hợp:**

1. **User gửi message** → Socket.IO/HTTP
2. **IntelligentCoordinator** phân loại intent (NLP)
3. **PlannerAgent** lập kế hoạch, quyết định gọi tools
4. **RAG Retrieval**: Search tours từ PostgreSQL
5. **Function Calling**: UserProxy thực thi search
6. **LLM Generation**: RecommendationAgent tạo câu trả lời
7. **Response** được gửi về user qua Socket.IO

**Kết luận Chương 2:**

Chương này đã trình bày các cơ sở lý thuyết quan trọng:

- Chatbot và LLMs (GPT-4)
- RAG để giải quyết hallucination và knowledge cutoff
- Multi-Agent Systems để chia nhỏ tác vụ phức tạp
- NLP cho tiếng Việt
- Web technologies (FastAPI, Socket.IO, PostgreSQL)

Các công nghệ này sẽ được tích hợp trong Chương 3 (Thiết kế hệ thống) và Chương 4 (Triển khai).

---

## CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

(Sẽ được bổ sung trong các phần tiếp theo...)

---

## CHƯƠNG 4: TRIỂN KHAI HỆ THỐNG

(Sẽ được bổ sung trong các phần tiếp theo...)

---

## CHƯƠNG 5: ĐÁNH GIÁ VÀ KẾT QUẢ

(Sẽ được bổ sung trong các phần tiếp theo...)

---

## CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

(Sẽ được bổ sung trong các phần tiếp theo...)

---

## TÀI LIỆU THAM KHẢO

1. Lewis, P., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks". NeurIPS 2020.

2. Wu, Q., et al. (2023). "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation". Microsoft Research.

3. Brown, T., et al. (2020). "Language Models are Few-Shot Learners". OpenAI.

4. FastAPI Documentation. https://fastapi.tiangolo.com/

5. Socket.IO Documentation. https://socket.io/docs/

6. SQLAlchemy Documentation. https://docs.sqlalchemy.org/

---

**Sinh viên thực hiện**: Hoàng Công Vũ  
**Giảng viên hướng dẫn**: [Tên GVHD]  
**Thời gian thực hiện**: [Thời gian]  
**Địa điểm**: [Trường/Khoa]
