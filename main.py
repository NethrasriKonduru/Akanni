from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import os

from database import get_db, Base, engine
from routers import meetings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Department Services API",
    description="API for managing departments, services, and scheduling meetings",
    version="1.0.0"
)

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
app.include_router(meetings.router, prefix="/api/v1", tags=["Meetings"])

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Welcome to Department Services API",
        "docs": "/docs",
        "redoc": "/redoc"
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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)