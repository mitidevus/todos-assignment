import enum
from database import Base
from sqlalchemy import Column, String, Uuid, Enum, ForeignKey
from .base_entity import BaseEntity

class TaskStatus(enum.Enum):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    
class TaskPriority(enum.Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    summary = Column(String)
    description = Column(String)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.LOW)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)