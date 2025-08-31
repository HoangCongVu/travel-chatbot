from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import alembic.config

from env import env
from app_environment import AppEnvironment


def create_app() -> FastAPI:
    app = FastAPI(debug=env.DEBUG)

    @app.get("/")
    def read_root():
        return {"message": "Hello FastAPI 🚀"}

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

    return app


app = create_app()
