from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from sqlalchemy.orm import relationship

from db import Base


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    name = Column(String(50))
    number = Column(String(20))
    username = Column(String(50), unique=True)
    password = Column(String(200))
    status = Column(Boolean, default=True)
    token = Column(String(400), default='')