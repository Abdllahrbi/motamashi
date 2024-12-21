from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class SubscriptionTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class UserBase(BaseModel):
    email: str
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    subscription_tier: SubscriptionTier
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkspaceCreate(WorkspaceBase):
    pass

class Workspace(WorkspaceBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BoardBase(BaseModel):
    name: str
    description: Optional[str] = None
    workspace_id: int
    view_type: str = "kanban"

class BoardCreate(BoardBase):
    pass

class Board(BoardBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    board_id: int
    status: str = "todo"
    priority: int = 0
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    assignee_id: Optional[int]
    ai_score: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True

class LabelBase(BaseModel):
    name: str
    color: str

class LabelCreate(LabelBase):
    pass

class Label(LabelBase):
    id: int

    class Config:
        from_attributes = True

class TaskLabel(BaseModel):
    task_id: int
    label_id: int

    class Config:
        from_attributes = True

class TaskRecommendation(BaseModel):
    title: str
    description: str

class AIAnalytics(BaseModel):
    id: int
    user_id: int
    workspace_id: int
    analysis_type: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
