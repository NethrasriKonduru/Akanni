from sqlalchemy import Column, Integer, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Department(Base):
    __tablename__ = 'dept'
    
    Dept_id = Column(Integer, primary_key=True, autoincrement=True)
    Dept_name = Column(Text)
    
    # Relationship with services through the dept_service association table
    services = relationship("Service", secondary="dept_service", back_populates="departments")

class Service(Base):
    __tablename__ = 'services'
    
    service_id = Column(Integer, primary_key=True, autoincrement=True)
    Service_name = Column(Text)
    
    # Relationship with departments through the dept_service association table
    departments = relationship("Department", secondary="dept_service", back_populates="services")
