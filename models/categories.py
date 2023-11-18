from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, and_
from sqlalchemy.orm import relationship, backref

from db import Base


class Categories(Base):
    __tablename__ = "Categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    comment = Column(Text)
    user_id = Column(Integer)

    category_items = relationship('CategoryItems', back_populates='category')


class CategoryItems(Base):
    __tablename__ = "CategoryItems"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    category_id = Column(Integer, ForeignKey("Categories.id"))
    user_id = Column(Integer, ForeignKey("Users.id"))
    category = relationship('Categories', back_populates='category_items')