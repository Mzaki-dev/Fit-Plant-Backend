from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import enum

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskBase(BaseModel):
    title: str
    description: str
    crop_type: str
    due_date: datetime
    assigned_to: int
    status: TaskStatus = TaskStatus.pending

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    crop_type: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    status: Optional[TaskStatus] = None

class Task(TaskBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskWithWorker(BaseModel):
    id: int
    title: str
    description: str
    crop_type: str
    due_date: datetime
    assigned_to: int
    status: TaskStatus
    created_by: int
    created_at: datetime
    updated_at: datetime
    worker_name: str

    class Config:
        from_attributes = True

class PaginatedTasks(BaseModel):
    tasks: list[TaskWithWorker]
    total: int
    page: int
    limit: int
    total_pages: int

    class Config:
        from_attributes = True