from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, and_
from sqlalchemy.orm import relationship, backref

from db import Base
from models.projects import Projects


class Targets(Base):
    __tablename__ = "Targets"
    id = Column(Integer, primary_key=True)
    link = Column(String(250))
    count_watches = Column(Integer, default=0)
    status = Column(Boolean)
    comment = Column(Text)
    project_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("Users.id"))

    project = relationship('Projects', foreign_keys=[project_id],
                           primaryjoin=lambda: and_(Projects.id == Targets.project_id),
                           backref=backref("projects"))
