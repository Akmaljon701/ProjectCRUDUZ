from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, and_
from sqlalchemy.orm import relationship, backref

from db import Base


class Categories(Base):
    __tablename__ = "Categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    comment = Column(Text)
    user_id = Column(Integer)


class CategoryItems(Base):
    __tablename__ = "CategoryItems"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    category_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("Users.id"))
    ordinal_number = Column(Integer)

    category = relationship('Categories', foreign_keys=[category_id],
                            primaryjoin=lambda: and_(Categories.id == CategoryItems.category_id),
                            backref=backref("category_items"))
