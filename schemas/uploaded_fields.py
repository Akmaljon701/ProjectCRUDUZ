from fastapi import File
from pydantic import BaseModel, Field


class FileBySourceId(BaseModel):
    source_id: int = File(ge=0)