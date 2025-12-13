from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..crud.user import get_workers, create_user, update_user, delete_user, authenticate_user
from ..schemas.user import User, UserCreate, UserUpdate, PaginatedWorkers, Token
from ..auth.auth import get_current_admin, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os
import shutil
from ..models.task import Task

router = APIRouter()

@router.get("/workers/", response_model=PaginatedWorkers)
def read_workers(page: int = 1, limit: int = 10, search: str = None, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than 0")
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    workers, total = get_workers(db, page=page, limit=limit, search=search)
    total_pages = (total + limit - 1) // limit  # Ceiling division
    return PaginatedWorkers(
        workers=workers,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )

@router.post("/workers/", response_model=User)
def create_worker(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    fields: str = Form(None),
    role: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    profile_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    if role != "worker":
        raise HTTPException(status_code=400, detail="Role must be worker")
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    user_data = {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "fields": fields,
        "role": role,
        "password": password,
        "confirm_password": confirm_password
    }
    user_obj = UserCreate(**user_data)
    
    # Create user first
    db_user = create_user(db=db, user=user_obj)
    
    # Handle image upload
    if profile_image:
        # Create uploads directory if not exists
        uploads_dir = "uploads"
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        # Create worker folder
        worker_dir = os.path.join(uploads_dir, f"worker_{db_user.id}")
        if not os.path.exists(worker_dir):
            os.makedirs(worker_dir)
        
        # Save image
        file_path = os.path.join(worker_dir, profile_image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile_image.file, buffer)
        
        # Update user with image path
        db_user.image_path = file_path
        db.commit()
        db.refresh(db_user)
    
    return db_user

@router.put("/workers/{user_id}", response_model=User)
def update_worker(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    if user_update.full_name is not None and not user_update.full_name.strip():
        raise HTTPException(status_code=400, detail="Full name cannot be empty")
    db_user = update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/workers/{user_id}")
def delete_worker(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    # Check if worker has assigned tasks
    task_count = db.query(Task).filter((Task.assigned_to == user_id) | (Task.created_by == user_id)).count()
    if task_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete worker with assigned or created tasks")
    
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user