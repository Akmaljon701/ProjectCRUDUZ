from pydantic import BaseModel, validator, Field
from typing import Optional, List
from sqlalchemy.orm import Session


class CategoryCreate(BaseModel):
    name: str
    comment: str


class CategoryItemsCreate(BaseModel):
    category_id: int
    text: str
    ordinal_number: int


class CategoryUpdate(BaseModel):
    category_id: int
    name: str
    comment: str


class CategoryItemUpdate(BaseModel):
    category_item_id: int
    text: str
