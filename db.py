from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from env import env

db = create_engine(
    f"postgresql://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}",
    pool_pre_ping=True,
    pool_recycle=1800,
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=db)
Base = declarative_base()
