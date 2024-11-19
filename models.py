from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from database import Base

# We import Base which is created from database.py 
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    status = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)    