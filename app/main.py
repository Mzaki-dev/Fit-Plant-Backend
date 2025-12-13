from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from .database import engine, Base, SessionLocal
from .routers.users import router
from .routers.tasks import router as tasks_router
from .routers.predictions import router as predictions_router
from .routers.reports import router as reports_router
from .dependencies import get_db

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "uploads")), name="uploads")

# Mount static files for processed images
app.mount("/processed_images", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "processed_images")), name="processed_images")

app.include_router(router, prefix="/api", tags=["users"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(predictions_router, prefix="/api", tags=["predictions"])
app.include_router(reports_router, prefix="/api/reports", tags=["reports"])