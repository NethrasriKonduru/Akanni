import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from sqlalchemy.orm import Session
from models.oauth_token import OAuthToken
from config import GOOGLE_CLIENT_CONFIG

# OAuth 2.0 scopes for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.events']

class GoogleAuthService:
    def __init__(self, db: Session):
        self.db = db
        self.client_config = GOOGLE_CLIENT_CONFIG

    def get_authorization_url(self, redirect_uri: str, user_id: str) -> str:
        """Generate Google OAuth URL"""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        
        # Include the user ID in the state parameter
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent',
            state=user_id
        )
        return auth_url

    def save_credentials(self, code: str, redirect_uri: str) -> OAuthToken:
        """Exchange authorization code for tokens and save them"""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        
        # Exchange code for tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Save or update tokens in database
        token_data = {
            'access_token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': self.client_config['web']['client_secret'],
            'scopes': json.dumps(credentials.scopes),
            'expiry': credentials.expiry
        }
        
        # Get user_id from state (passed during authorization)
        user_id = flow.session.state
        
        # Check if token exists for user
        token = self.db.query(OAuthToken).filter_by(user_id=user_id).first()
        
        if token:
            # Update existing token
            for key, value in token_data.items():
                setattr(token, key, value)
        else:
            # Create new token
            token = OAuthToken(user_id=user_id, **token_data)
            self.db.add(token)
        
        self.db.commit()
        self.db.refresh(token)
        return token

    def get_credentials(self, user_id: str) -> Credentials:
        """Get valid credentials for a user, refreshing if necessary"""
        token = self.db.query(OAuthToken).filter_by(user_id=user_id).first()
        if not token:
            raise ValueError("No credentials found for user")
        
        creds = Credentials(
            token=token.access_token,
            refresh_token=token.refresh_token,
            token_uri=token.token_uri,
            client_id=token.client_id,
            client_secret=token.client_secret,
            scopes=json.loads(token.scopes) if token.scopes else None,
            expiry=token.expiry
        )
        
        # Refresh token if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Update the stored token
            token.access_token = creds.token
            token.expiry = creds.expiry
            self.db.commit()
        
        return creds
