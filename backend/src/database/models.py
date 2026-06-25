from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text
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

    datasets = relationship('Dataset', back_populates="user")
    queries = relationship('QueryHistory', back_populates="user")


class Dataset(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String(100), nullable=False)
    file_path = Column(String(100), nullable=False, unique=True)
    uploaded_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship('User', back_populates='datasets')
    queries = relationship('QueryHistory', back_populates="dataset")


class QueryHistory(Base):
    __tablename__ = 'query_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    dataset_id = Column(Integer, ForeignKey('datasets.id'), nullable=False)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship('User', back_populates="queries")
    dataset = relationship('Dataset', back_populates="queries")