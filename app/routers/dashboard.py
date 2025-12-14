from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..dependencies import get_db
from ..auth.auth import get_current_admin
from ..models.task import Task, TaskStatus
from ..models.user import User
from datetime import datetime, timedelta
from typing import List, Dict

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    # Total tasks
    total_tasks = db.query(func.count(Task.id)).scalar()
    
    # Pending tasks
    pending_tasks = db.query(func.count(Task.id)).filter(Task.status == TaskStatus.pending).scalar()
    
    # Completed tasks
    completed_tasks = db.query(func.count(Task.id)).filter(Task.status == TaskStatus.completed).scalar()
    
    # Active workers
    active_workers = db.query(func.count(User.id)).filter(User.role == "worker", User.is_active == True).scalar()
    
    return {
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "active_workers": active_workers
    }

@router.get("/weekly-task-overview")
def get_weekly_task_overview(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    # Get tasks created in the last 7 days, grouped by day
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    
    tasks = db.query(
        func.date(Task.created_at).label('date'),
        func.count(Task.id).label('count')
    ).filter(
        Task.created_at >= week_ago
    ).group_by(
        func.date(Task.created_at)
    ).all()
    
    # Fill missing days with 0
    overview = {}
    for i in range(7):
        day = week_ago + timedelta(days=i)
        overview[day.isoformat()] = 0
    
    for task in tasks:
        overview[task.date.isoformat()] = task.count
    
    return overview

@router.get("/weekly-completion-rate")
def get_weekly_completion_rate(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    # Completion rates for the last 4 weeks
    today = datetime.utcnow().date()
    rates = {}
    for i in range(4):
        week_start = today - timedelta(days=today.weekday() + 7*i)  # Monday of each week
        week_end = week_start + timedelta(days=6)
        
        total_tasks_week = db.query(func.count(Task.id)).filter(
            func.date(Task.created_at) >= week_start,
            func.date(Task.created_at) <= week_end
        ).scalar()
        
        completed_tasks_week = db.query(func.count(Task.id)).filter(
            Task.status == TaskStatus.completed,
            func.date(Task.created_at) >= week_start,
            func.date(Task.created_at) <= week_end
        ).scalar()
        
        if total_tasks_week == 0:
            rate = 0.0
        else:
            rate = (completed_tasks_week / total_tasks_week) * 100
        
        week_label = f"{week_start.year}-W{week_start.isocalendar()[1]}"
        rates[week_label] = round(rate, 2)
    
    return rates