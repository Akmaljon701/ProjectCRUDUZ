from pydantic import BaseModel, Field


class TargetCreate(BaseModel):
    status: bool
    comment: str
    project_id: int = Field(ge=0.1)


class TargetUpdate(BaseModel):
    target_id: int
    status: bool
    comment: str
    project_id: int = Field(ge=0.1)
