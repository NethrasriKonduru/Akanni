from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import os

from database import get_db, Base, engine
from routers import auth_router, calendar_router
from routers.testimonials import router as testimonials_router
from routers.testimonial_api import router as testimonial_api_router
from auth_utils import get_current_active_user, oauth2_scheme
from models.user import User

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Google Calendar Integration API",
    description="API for Google Calendar integration with OAuth2 authentication",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# Mount uploads directory for serving uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Templates
templates = Jinja2Templates(directory="templates")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ServiceBase(BaseModel):
    service_id: int
    Service_name: str

    class Config:
        orm_mode = True

class DepartmentBase(BaseModel):
    Dept_id: int
    Dept_name: str
    services: List[ServiceBase] = []

    class Config:
        orm_mode = True

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(calendar_router, prefix="/api/v1")
app.include_router(testimonials_router)
app.include_router(testimonial_api_router)

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Welcome to Google Calendar Integration API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Protected route example
@app.get("/api/v1/protected")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    return {
        "message": "This is a protected route",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "is_active": current_user.is_active
        }
    }

@app.get("/departments/", response_model=List[DepartmentBase])
async def get_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = db.query(models.Department).offset(skip).limit(limit).all()
    return departments

@app.get("/services/", response_model=List[ServiceBase])
async def get_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    services = db.query(models.Service).offset(skip).limit(limit).all()
    return services

@app.get("/departments/{dept_id}", response_model=DepartmentBase)
async def get_department(dept_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(models.Department.Dept_id == dept_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@app.get("/services/{service_id}", response_model=ServiceBase)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.service_id == service_id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # default to 8000 locally
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)