from fastapi import APIRouter, Depends, HTTPException
from ..schemas.user import User, TaskCounts
from ..auth.auth import get_current_active_user
import os
from fastapi.responses import FileResponse
from ..crud.task import get_task_counts_for_user
from ..dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")

@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/me/image")
async def get_user_image(current_user: User = Depends(get_current_active_user)):
    if not current_user.image_path or not os.path.exists(current_user.image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(current_user.image_path)

@router.get("/me/tasks/counts", response_model=TaskCounts)
async def get_user_task_counts(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    counts = get_task_counts_for_user(db, current_user.id)
    return TaskCounts(**counts)