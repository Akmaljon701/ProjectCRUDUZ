from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class UploadedFiles(Base):
    __tablename__ = "UploadedFiles"
    id = Column(Integer, primary_key=True)
    file = Column(String(250))
    comment = Column(Text)
    source = Column(String(50))
    source_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("Users.id"))
