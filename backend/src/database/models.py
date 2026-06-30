from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    datasets = relationship('Dataset', back_populates="user", cascade="all, delete-orphan")
    chats = relationship('ChatSession', back_populates="user", cascade="all, delete-orphan")


class Dataset(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String(100), nullable=False)
    file_path = Column(String(100), nullable=False, unique=True)
    uploaded_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship('User', back_populates='datasets')
    chats = relationship('ChatSession', back_populates="dataset")


class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    title = Column(String(100), default='New Chat', nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship('User', back_populates="chats")
    dataset = relationship('Dataset', back_populates="chats")
    history = relationship('QueryHistory', back_populates="chat", cascade="all, delete-orphan")


class QueryHistory(Base):
    __tablename__ = 'query_history'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    generated_code = Column(Text, nullable=True)
    execution_time_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    chat = relationship('ChatSession', back_populates="history")