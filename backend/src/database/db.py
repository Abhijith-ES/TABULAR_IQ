from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///tabulariq.db"

engine = create_engine(
    DATABASE_URL,
    connect_args = {
        "check_same_thread" : False
    }
)

SessionLocal = sessionmaker(
    bind = engine,
    auto_commit = False,
    auto_flush = False
)

Base = declarative_base()