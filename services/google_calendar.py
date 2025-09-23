import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "timezone": "Asia/Kolkata",
    "conference_solution": {
        "type": "hangoutsMeet",
        "name": "Google Meet"
    },
    "reminders": {
        "useDefault": True
    },
    "conference_data_version": 1
}

class GoogleCalendarService:
    """Service for interacting with Google Calendar API with OAuth token management."""
    
    def __init__(self, oauth_service, user_id: str):
        """
        Initialize the Google Calendar service.
        
        Args:
            oauth_service: Instance of OAuthService for token management
            user_id: ID of the user whose calendar we're accessing
        """
        self.oauth_service = oauth_service
        self.user_id = user_id
        self.service = self._get_calendar_service()
    
    def _get_calendar_service(self):
        """Get an authenticated Google Calendar service instance."""
        creds = self.oauth_service.get_credentials(self.user_id)
        if not creds:
            logger.error("No valid credentials available")
            raise ValueError("Authentication required. Please complete OAuth flow first.")
        
        try:
            return build("calendar", "v3", credentials=creds)
        except Exception as e:
            logger.error(f"Failed to create Calendar service: {str(e)}")
            raise
    
    def create_meeting(self, event_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new calendar event with Google Meet.
        
        Args:
            event_config: Dictionary containing event configuration
                Required keys: summary, start_time, end_time
                Optional keys: description, attendees, timezone, location
                
        Returns:
            Dictionary containing event details including Meet link
        """
        try:
            # Merge with default config
            config = {**DEFAULT_CONFIG, **event_config}
            
            # Prepare event data
            event = {
                "summary": config["summary"],
                "description": config.get("description", ""),
                "start": {
                    "dateTime": config["start_time"],
                    "timeZone": config["timezone"]
                },
                "end": {
                    "dateTime": config["end_time"],
                    "timeZone": config["timezone"]
                },
                "conferenceData": {
                    "createRequest": {
                        "requestId": f"meet-{self.user_id}-{int(datetime.now().timestamp())}",
                        "conferenceSolutionKey": {"type": config["conference_solution"]["type"]},
                        "requestedConferenceSolutionKey": {
                            "type": config["conference_solution"]["type"]
                        },
                    }
                },
                "reminders": config["reminders"]
            }
            
            # Add attendees if provided
            if "attendees" in config and config["attendees"]:
                event["attendees"] = [{"email": email} for email in config["attendees"]]
            
            # Create the event
            event_result = (
                self.service.events()
                .insert(
                    calendarId="primary",
                    body=event,
                    conferenceDataVersion=config["conference_data_version"]
                )
                .execute()
            )
            
            logger.info(f"Created event: {event_result.get('htmlLink')}")
            
            # Extract meet link
            meet_link = None
            if event_result.get('conferenceData', {}).get('entryPoints'):
                for entry in event_result['conferenceData']['entryPoints']:
                    if entry.get('entryPointType') == 'video':
                        meet_link = entry.get('uri')
                        break
            
            return {
                "event_id": event_result.get('id'),
                "html_link": event_result.get('htmlLink'),
                "meet_link": meet_link,
                "start_time": event_result.get('start', {}).get('dateTime'),
                "end_time": event_result.get('end', {}).get('dateTime'),
                "status": event_result.get('status')
            }
            
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            raise
    
    def list_upcoming_events(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """List upcoming events from the user's calendar."""
        try:
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = (
                self.service.events()
                .list(
                    calendarId='primary',
                    timeMin=now,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy='startTime'
                )
                .execute()
            )
            return events_result.get('items', [])
            
        except Exception as e:
            logger.error(f"Error listing events: {str(e)}")
            raise
