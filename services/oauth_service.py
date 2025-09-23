import os
import json
import logging
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy.orm import Session

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from models.oauth_token import OAuthToken

# Configure logging
logger = logging.getLogger(__name__)

# OAuth 2.0 scopes for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

class OAuthService:
    def __init__(self, db):
        self.db = db
        # Use absolute path to client_secret.json
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.credentials_path = os.path.join(base_dir, 'client_secret.json')
        with open(self.credentials_path) as f:
            self.client_config = json.load(f)['web']

    def get_authorization_url(self, redirect_uri: str, user_id: str = "") -> str:
        """Generate Google OAuth URL
        
        Args:
            redirect_uri: The URI to redirect to after authorization
            user_id: Optional user ID to include in the state parameter
            
        Returns:
            str: The authorization URL
        """
        flow = Flow.from_client_config(
            {"web": self.client_config},
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )

        # Include user_id in the state parameter if provided
        state = user_id if user_id else ""
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state,
            prompt='consent'  # Force consent prompt
        )
        return auth_url

    def save_credentials(self, user_id: str, code: str, redirect_uri: str) -> bool:
        """Exchange code for tokens and save to DB"""
        try:
            logger.info(f"Exchanging code for tokens for user_id: {user_id}")
            flow = Flow.from_client_config(
                {"web": self.client_config},
                scopes=SCOPES,
                redirect_uri=redirect_uri
            )
            
            # Fetch the token
            flow.fetch_token(code=code)
            creds = flow.credentials
            
            if not creds or not creds.token:
                logger.error("Failed to get valid credentials from OAuth flow")
                raise Exception("Failed to get valid credentials from OAuth flow")
                
            logger.info(f"Successfully obtained credentials for user_id: {user_id}")
            
            token_data = {
                'token': creds.token,
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': self.client_config['client_secret'],
                'scopes': creds.scopes,
                'expiry': creds.expiry.isoformat() if creds.expiry else None
            }
            
            self._save_token(user_id, token_data)
            logger.info(f"Successfully saved token for user_id: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error in save_credentials for user_id {user_id}: {str(e)}")
            raise

    def get_credentials(self, user_id: str) -> Credentials | None:
        """Return valid credentials, refresh if needed"""
        try:
            logger.info(f"Getting credentials for user_id: {user_id}")
            token = self.db.query(OAuthToken).filter(OAuthToken.user_id == user_id).first()
            if not token:
                logger.warning(f"No OAuth token found for user_id: {user_id}")
                return None

            logger.debug(f"Found token for user_id: {user_id}, expired: {token.expiry < datetime.utcnow() if token.expiry else 'no expiry'}")
            
            try:
                scopes = json.loads(token.scopes) if token.scopes else SCOPES
            except json.JSONDecodeError:
                logger.warning(f"Invalid scopes format for user_id {user_id}, using default scopes")
                scopes = SCOPES

            creds = Credentials(
                token=token.access_token,
                refresh_token=token.refresh_token,
                token_uri=token.token_uri,
                client_id=token.client_id,
                client_secret=token.client_secret,
                scopes=scopes
            )

            if creds.expired and creds.refresh_token:
                logger.info(f"Refreshing expired token for user_id: {user_id}")
                try:
                    creds.refresh(Request())
                    logger.info("Token refresh successful")
                    self._save_token(user_id, {
                        'token': creds.token,
                        'refresh_token': creds.refresh_token or token.refresh_token,
                        'token_uri': creds.token_uri,
                        'client_id': creds.client_id,
                        'client_secret': creds.client_secret,
                        'scopes': creds.scopes,
                        'expiry': creds.expiry.isoformat() if creds.expiry else None
                    })
                except Exception as refresh_error:
                    logger.error(f"Failed to refresh token for user_id {user_id}: {str(refresh_error)}")
                    return None

            return creds if not creds.expired else None
            
        except Exception as e:
            logger.error(f"Error in get_credentials for user_id {user_id}: {str(e)}")
            return None

    def _save_token(self, user_id: str, token_data: dict):
        """Create or update token in DB"""
        token = self.db.query(OAuthToken).filter(OAuthToken.user_id == user_id).first()
        if token:
            token.access_token = token_data['token']
            if 'refresh_token' in token_data and token_data['refresh_token']:
                token.refresh_token = token_data['refresh_token']
            token.token_uri = token_data['token_uri']
            token.client_id = token_data['client_id']
            token.client_secret = token_data['client_secret']
            token.scopes = json.dumps(token_data['scopes'])
            token.expiry = datetime.fromisoformat(token_data['expiry'])
        else:
            token = OAuthToken(
                user_id=user_id,
                access_token=token_data['token'],
                refresh_token=token_data.get('refresh_token'),
                token_uri=token_data['token_uri'],
                client_id=token_data['client_id'],
                client_secret=token_data['client_secret'],
                scopes=json.dumps(token_data['scopes']),
                expiry=datetime.fromisoformat(token_data['expiry'])
            )
            self.db.add(token)
        self.db.commit()

class CalendarService:
    def __init__(self, oauth_service: OAuthService, db: Session):
        self.oauth_service = oauth_service
        self.db = db

    def create_meet_event(
        self, user_id: str, summary: str, start_time: datetime, end_time: datetime, attendees: list
    ) -> Optional[Dict[str, Any]]:
        """Create a Google Calendar event with a Meet link for a user."""
        creds = self.oauth_service.get_credentials(user_id)
        if not creds:
            raise Exception("No valid credentials found for user")

        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": summary,
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Kolkata"},
            "attendees": [{"email": a} for a in attendees],
            "conferenceData": {
                "createRequest": {"requestId": f"meet-{datetime.now().timestamp()}"}
            },
        }

        created_event = (
            service.events()
            .insert(calendarId="primary", body=event, conferenceDataVersion=1)
            .execute()
        )

        return {
            "calendar_event": created_event.get("htmlLink"),
            "meet_link": created_event["conferenceData"]["entryPoints"][0]["uri"],
        }
