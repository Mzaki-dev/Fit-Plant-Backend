from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..crud.task import get_tasks, create_task, update_task, delete_task
from ..schemas.task import Task, TaskCreate, TaskUpdate, TaskWithWorker, PaginatedTasks
from ..auth.auth import get_current_admin
from ..models.user import User

router = APIRouter()

@router.get("/tasks/", response_model=PaginatedTasks)
def read_tasks(page: int = 1, limit: int = 10, search: str = None, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than 0")
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    tasks, total = get_tasks(db, page=page, limit=limit, search=search)
    total_pages = (total + limit - 1) // limit  # Ceiling division
    return PaginatedTasks(
        tasks=tasks,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )

@router.post("/tasks/", response_model=Task)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    # Check if assigned_to is a worker
    assigned_user = db.query(User).filter(User.id == task.assigned_to, User.role == "worker").first()
    if not assigned_user:
        raise HTTPException(status_code=400, detail="Assigned user must be a worker")
    db_task = create_task(db=db, task=task, created_by=current_user.id)
    return db_task

@router.put("/tasks/{task_id}", response_model=Task)
def update_existing_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    if task_update.assigned_to:
        assigned_user = db.query(User).filter(User.id == task_update.assigned_to, User.role == "worker").first()
        if not assigned_user:
            raise HTTPException(status_code=400, detail="Assigned user must be a worker")
    db_task = update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/tasks/{task_id}")
def delete_existing_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    db_task = delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}