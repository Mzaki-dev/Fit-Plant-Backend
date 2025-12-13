from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import enum

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskSeverity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class TaskBase(BaseModel):
    title: str
    description: str
    crop_type: str
    due_date: datetime
    assigned_to: int
    status: TaskStatus = TaskStatus.pending
    severity: TaskSeverity = TaskSeverity.low

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    crop_type: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    status: Optional[TaskStatus] = None
    severity: Optional[TaskSeverity] = None
    image_path: Optional[str] = None
    plant_condition: Optional[str] = None

class Task(TaskBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    image_path: Optional[str] = None
    plant_condition: Optional[str] = None
    image_name: Optional[str] = None

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
    severity: TaskSeverity
    created_by: int
    created_at: datetime
    updated_at: datetime
    worker_name: str
    worker_image_path: Optional[str] = None
    image_path: Optional[str] = None
    plant_condition: Optional[str] = None

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