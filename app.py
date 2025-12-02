from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import socketio
import alembic.config
from env import env
from app_environment import AppEnvironment
from controllers import (admin,
file,
upload_file,
upload_file_agent,
chatbot,
user,
chat,
message,
tour_type,
tour,
visa_price,
price_by_date,
price_by_package,
tour_departure,
tour_destination,
tour_highlight_location,
departure_schedule,
recurring_schedule,
specific_departure,
agent_tour,
tour_search,
facebook_webhook,
follow_up_settings
)
from utils.socket_manager import sio

def create_app() -> FastAPI:
    app = FastAPI(
        debug=env.DEBUG,
        title="Travel Chatbot API 🚀",
    #         contact={
    #     "name": "Albin",
    #     "url": "https://your-website.com",
    #     "email": "vu27042003@gmail.com",
    # },
    )

    @app.get("/")
    def read_root():
        return {"message": "Hello Albin 🚀"}

    # 👉 Chỉ migrate DB khi đang ở local/dev
    if AppEnvironment.is_local_env(env.APP_ENV):
        try:
            alembic.config.main(argv=["--raiseerr", "upgrade", "head"])
            print("✅ Database migrated to latest version.")
        except Exception as e:
            print(f"⚠️ Database migration failed: {e}")

        # Cho phép CORS khi dev
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    app.include_router(admin.router, prefix="/api")
    app.include_router(file.router, prefix="/api")    
    app.include_router(upload_file.router, prefix="/api")
    app.include_router(upload_file_agent.router, prefix="/api")
    app.include_router(chatbot.router, prefix="/api")
    app.include_router(user.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")
    app.include_router(message.router, prefix="/api")
    app.include_router(tour_type.router, prefix="/api")
    app.include_router(tour.router, prefix="/api")
    app.include_router(visa_price.router, prefix="/api")
    app.include_router(price_by_date.router, prefix="/api")
    app.include_router(price_by_package.router, prefix="/api")
    app.include_router(tour_departure.router, prefix="/api")
    app.include_router(tour_destination.router, prefix="/api")
    app.include_router(tour_highlight_location.router, prefix="/api")
    app.include_router(departure_schedule.router, prefix="/api")
    app.include_router(recurring_schedule.router, prefix="/api")
    app.include_router(specific_departure.router, prefix="/api")
    app.include_router(agent_tour.router, prefix="/api")
    app.include_router(tour_search.router, prefix="/api")
    app.include_router(facebook_webhook.router) 
    app.include_router(follow_up_settings.router, prefix="/api")
    
    # 🔥 Mount Socket.IO vào FastAPI (support fastapi dev)
    socket_asgi_app = socketio.ASGIApp(
        socketio_server=sio,
        socketio_path=""  # Empty vì đã mount tại /socket.io
    )
    app.mount("/socket.io", socket_asgi_app)
    
    return app


app = create_app()
