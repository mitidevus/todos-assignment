from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from models import CompanyViewModel

class UserModel(BaseModel):
    username: str
    email: Optional[str] = None
    first_name: str
    last_name: str
    password: str
    company_id: Optional[UUID] = None
    
class UpdateUserModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]

class UserBaseModel(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True

class UserViewModel(UserBaseModel):
    is_admin: bool
    is_active: bool
    company_id: UUID | None = None
    company: CompanyViewModel | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None