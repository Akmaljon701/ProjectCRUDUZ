from fastapi import Depends, HTTPException
from pydantic import BaseModel, validator, Field
from typing import Optional, List
from sqlalchemy.orm import Session
from db import get_db, SessionLocal
from models.users import Users

db: Session = SessionLocal()


class UserBase(BaseModel):
    name: str
    username: str
    role: str
    status: bool


class UserCreate(UserBase):
    password: str
    number: str


class UserUpdate(UserBase):
    id: int
    password: str
    number: str


class Token(BaseModel):
    access_token = str
    token = str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserCurrent(BaseModel):
    id: int
    name: str
    username: str
    password: str
    role: str
    status: bool
