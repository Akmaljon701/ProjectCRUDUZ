from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from db import Base
from models.users import Users


class Projects(Base):
    __tablename__ = "Projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    comment = Column(Text)
    status = Column(Boolean, default=True)
    url = Column(String(250))
    source_id = Column(Integer)
    user_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Projects.user_id),
                        backref=backref("projects"))
