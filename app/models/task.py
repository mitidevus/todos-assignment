from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from schemas import TaskStatus, TaskPriority

class TaskModel(BaseModel):
    summary: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=255)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.LOW)

class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True