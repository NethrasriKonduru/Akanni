from sqlalchemy import Column, Integer, String, Boolean, DateTime, event
from sqlalchemy.orm import relationship
from datetime import datetime
from passlib.context import CryptContext

from .base import Base

# Constants for field lengths
EMAIL_LENGTH = 255
NAME_LENGTH = 100
PASSWORD_LENGTH = 255

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(EMAIL_LENGTH), unique=True, index=True, nullable=False)
    full_name = Column(String(NAME_LENGTH), nullable=True)
    hashed_password = Column(String(PASSWORD_LENGTH), nullable=True)  # Nullable for OAuth users
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    oauth_tokens = relationship("OAuthToken", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    @property
    def is_authenticated(self) -> bool:
        return self.is_active
    
    def set_password(self, password: str):
        """Set hashed password"""
        from auth_utils import get_password_hash
        self.hashed_password = get_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check password against stored hash"""
        from auth_utils import verify_password
        return verify_password(password, self.hashed_password)
