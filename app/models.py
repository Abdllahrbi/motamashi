from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum, Float
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from datetime import datetime
import enum
from .database import Base, engine

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SubscriptionTier(enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workspaces = relationship("Workspace", back_populates="owner")
    tasks = relationship("Task", back_populates="assignee")
    
    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)
    
    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="workspaces")
    boards = relationship("Board", back_populates="workspace")

class Board(Base):
    __tablename__ = "boards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    view_type = Column(String, default="kanban")  # kanban, list, calendar
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workspace = relationship("Workspace", back_populates="boards")
    tasks = relationship("Task", back_populates="board")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    board_id = Column(Integer, ForeignKey("boards.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="todo")
    priority = Column(Integer, default=0)
    due_date = Column(DateTime, nullable=True)
    ai_score = Column(Float, nullable=True)  # AI-generated priority score
    created_at = Column(DateTime, default=datetime.utcnow)
    
    board = relationship("Board", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")
    labels = relationship("TaskLabel", back_populates="task")

class Label(Base):
    __tablename__ = "labels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    color = Column(String)
    
    task_labels = relationship("TaskLabel", back_populates="label")

class TaskLabel(Base):
    __tablename__ = "task_labels"
    
    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    label_id = Column(Integer, ForeignKey("labels.id"), primary_key=True)
    
    task = relationship("Task", back_populates="labels")
    label = relationship("Label", back_populates="task_labels")

class AIAnalytics(Base):
    __tablename__ = "ai_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    analysis_type = Column(String)  # productivity, patterns, suggestions
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create all tables
Base.metadata.create_all(bind=engine)
