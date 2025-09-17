# Travel Chatbot

Dự án này là một chatbot hỗ trợ tư vấn du lịch, xây dựng với FastAPI, SQLAlchemy, Alembic và Poetry.

## Tính năng chính

- Chatbot tư vấn tour du lịch
- Quản lý người dùng, tin nhắn, lịch khởi hành, giá tour, điểm đến, loại tour, v.v.
- API RESTful cho các chức năng quản lý và truy vấn dữ liệu
- Quản lý cơ sở dữ liệu với Alembic và SQLAlchemy
- Cấu hình môi trường bằng Python-dotenv

## Cài đặt

1. Clone repository:
   ```sh
   git clone https://github.com/HoangCongVu/travel-chatbot.git
   cd travel-chatbot
   ```
2. Cài đặt dependencies bằng Poetry:
   ```sh
   poetry install
   ```
3. Tạo file `.env` và cấu hình thông tin kết nối database, API keys nếu cần.

## Chạy ứng dụng

```sh
poetry run fastapi dev app.py
```

Hoặc chạy bằng Uvicorn:

```sh
poetry run uvicorn app:app --reload
```

## Quản lý database

- Khởi tạo và migrate database:
  ```sh
  poetry run alembic upgrade head
  ```
- Tạo migration mới:
  ```sh
  poetry run alembic revision --autogenerate -m "Tên thay đổi"
  ```

## Cấu trúc thư mục

- `controllers/`: Xử lý logic API
- `models/`: Định nghĩa các model ORM
- `repositories/`: Truy vấn dữ liệu
- `services/`: Xử lý nghiệp vụ
- `app.py`: Khởi tạo ứng dụng FastAPI
- `db.py`: Kết nối database
- `alembic/`: Quản lý migration

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo pull request hoặc liên hệ qua email: vu27042003@gmail.com

## License

MIT
