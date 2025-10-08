from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import json

from .base import Base

# Constants for field lengths
USER_ID_LENGTH = 255
TOKEN_URI_LENGTH = 500
CLIENT_ID_LENGTH = 500
CLIENT_SECRET_LENGTH = 500

class OAuthToken(Base):
    __tablename__ = 'oauth_tokens'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, index=True, nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_uri = Column(String(TOKEN_URI_LENGTH), nullable=False)
    client_id = Column(String(CLIENT_ID_LENGTH), nullable=False)
    client_secret = Column(String(CLIENT_SECRET_LENGTH), nullable=False)
    scopes = Column(Text, nullable=False)  # Store as JSON string
    expiry = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="oauth_tokens")

    def to_dict(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'token_uri': self.token_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scopes': json.loads(self.scopes),
            'expiry': self.expiry.isoformat() if self.expiry else None
        }

    @classmethod
    def from_dict(cls, user_id: str, token_data: dict):
        return cls(
            user_id=user_id,
            access_token=token_data['access_token'],
            refresh_token=token_data.get('refresh_token'),
            token_uri=token_data['token_uri'],
            client_id=token_data['client_id'],
            client_secret=token_data['client_secret'],
            scopes=json.dumps(token_data['scopes']),
            expiry=datetime.strptime(token_data['expiry'], '%Y-%m-%dT%H:%M:%S.%f')
        )
    
    def is_expired(self):
        return datetime.utcnow() > self.expiry
    
    def needs_refresh(self):
        # Refresh token if it expires in the next 5 minutes
        return self.refresh_token and (self.expiry - datetime.utcnow()) < timedelta(minutes=5)
