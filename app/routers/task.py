from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from database import get_db_context
from services import task as TaskService
from services import auth as AuthService
from services.exception import *
from schemas import User
from models import TaskViewModel, TaskModel

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[TaskViewModel])
async def get_tasks(
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
    ):
        if not user.company_id:
            raise BadRequestError("User does not belong to any company")
    
        if not user.is_admin:
            return TaskService.get_my_tasks(db, user.id)

        return TaskService.get_all_tasks(db, user.company_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
async def create_task(
    request: TaskModel, 
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context),
    ):
        if not user:
            raise AccessDeniedError()

        user_id = user.id

        return TaskService.create_task(db, request, user_id)
