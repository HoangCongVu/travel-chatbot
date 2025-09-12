from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import alembic.config
from env import env
from app_environment import AppEnvironment
from controllers import (chatbot,
user,
chat,
tour_type,
visa_price,
departure_schedule,
)

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
        return {"message": "Hello Vũ 🚀"}

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
    app.include_router(chatbot.router, prefix="/api")
    app.include_router(user.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")
    app.include_router(tour_type.router, prefix="/api")
    app.include_router(visa_price.router, prefix="/api")
    app.include_router(departure_schedule.router, prefix="/api")
    return app


app = create_app()
