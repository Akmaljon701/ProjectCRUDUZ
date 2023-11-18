from pydantic import BaseModel, validator, Field
from typing import Optional, List
from sqlalchemy.orm import Session


class ProjectCreate(BaseModel):
    name: str
    comment: str
    status: bool
    url: str
    source_id: int


class ProjectUpdate(BaseModel):
    id: int = Field(ge=0.1)
    name: str
    comment: str
    status: bool
    url: str
    source_id: int
