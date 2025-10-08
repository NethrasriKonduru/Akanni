from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Testimonial(Base):
    __tablename__ = 'testimonials'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=True)
    company = Column(String(100), nullable=True)
    content = Column(Text, nullable=False)
    video_path = Column(String(255), nullable=True)  # Path to video file
    image_path = Column(String(255), nullable=True)  # Path to profile image
    rating = Column(Integer, nullable=True)  # Optional rating (1-5)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Testimonial {self.name} - {self.role} at {self.company}>"
