from sqlalchemy import Column, Integer, String
from .db import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    Task = Column(String, nullable=False)