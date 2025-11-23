from sqlalchemy.orm import Session, joinedload
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskWithWorker
from ..models.user import User

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, page: int = 1, limit: int = 10, search: str = None):
    query = db.query(Task)
    if search:
        query = query.filter(
            (Task.title.ilike(f"%{search}%")) |
            (Task.description.ilike(f"%{search}%")) |
            (Task.crop_type.ilike(f"%{search}%"))
        )
    total = query.count()
    offset = (page - 1) * limit
    tasks = query.options(joinedload(Task.assigned_user)).offset(offset).limit(limit).all()
    task_list = [
        TaskWithWorker(
            id=task.id,
            title=task.title,
            description=task.description,
            crop_type=task.crop_type,
            due_date=task.due_date,
            assigned_to=task.assigned_to,
            status=task.status,
            created_by=task.created_by,
            created_at=task.created_at,
            updated_at=task.updated_at,
            worker_name=task.assigned_user.full_name if task.assigned_user else ""
        )
        for task in tasks
    ]
    return task_list, total

def create_task(db: Session, task: TaskCreate, created_by: int):
    db_task = Task(
        title=task.title,
        description=task.description,
        crop_type=task.crop_type,
        due_date=task.due_date,
        assigned_to=task.assigned_to,
        status=task.status,
        created_by=created_by
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        for key, value in task_update.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def get_tasks_by_admin(db: Session, admin_id: int, skip: int = 0, limit: int = 100):
    # Assuming admin can see all tasks, or tasks created by them
    tasks = db.query(Task).options(joinedload(Task.assigned_user)).offset(skip).limit(limit).all()
    return [
        TaskWithWorker(
            id=task.id,
            title=task.title,
            description=task.description,
            crop_type=task.crop_type,
            due_date=task.due_date,
            assigned_to=task.assigned_to,
            status=task.status,
            created_by=task.created_by,
            created_at=task.created_at,
            updated_at=task.updated_at,
            worker_name=task.assigned_user.full_name if task.assigned_user else ""
        )
        for task in tasks
    ]