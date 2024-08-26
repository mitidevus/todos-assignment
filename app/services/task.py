from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from schemas import Task, User
from models.task import TaskModel
from services import user as UserService
from services.utils import get_current_utc_time
from services.exception import InvalidInputError

def get_all_tasks(db: Session, company_id) -> List[Task]:
    company_user_ids = db.query(User.id).filter(User.company_id == company_id).subquery()
    
    return db.query(Task).filter(Task.user_id.in_(company_user_ids)).all()

def get_my_tasks(db: Session, user_id: str) -> List[Task]:
    query = select(Task).filter(Task.user_id == user_id)
    
    return db.scalars(query).all()


def create_task(db: Session, data: TaskModel, user_id: str) -> Task:
    user = UserService.get_user_by_id(db, user_id)
        
    if user is None:
        raise InvalidInputError("Invalid user information")

    task = Task(**data.model_dump())
    task.user_id = user_id
    task.created_at = get_current_utc_time()
    task.updated_at = get_current_utc_time()

    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task