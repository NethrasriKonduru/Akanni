from datetime import datetime
from typing import Dict, List, Optional
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .google_auth import GoogleAuthService

class CalendarService:
    def __init__(self, db: Session):
        self.db = db
        self.auth_service = GoogleAuthService(db)

    async def create_event(
        self,
        user_id: str,
        summary: str,
        description: str,
        start_datetime: datetime,
        end_datetime: datetime,
        attendees: List[str] = None,
        timezone: str = "UTC"
    ) -> Dict:
        """Create a Google Calendar event with Google Meet"""
        try:
            # Get valid credentials
            creds = self.auth_service.get_credentials(user_id)
            
            # Create Google Calendar API client
            service = build('calendar', 'v3', credentials=creds)
            
            # Prepare event body
            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': timezone,
                },
                'conferenceData': {
                    'createRequest': {
                        'requestId': f"{user_id}_{int(datetime.utcnow().timestamp())}",
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                    }
                },
                'attendees': [{'email': email} for email in (attendees or [])],
            }
            
            # Create the event
            event = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1,
                sendUpdates='all'
            ).execute()
            
            return {
                'id': event['id'],
                'htmlLink': event.get('htmlLink'),
                'hangoutLink': event.get('hangoutLink'),
                'start': event['start'].get('dateTime', event['start'].get('date')),
                'end': event['end'].get('dateTime', event['end'].get('date')),
                'status': event.get('status')
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create event: {str(e)}"
            )

    async def list_events(
        self,
        user_id: str,
        time_min: datetime = None,
        max_results: int = 10,
        timezone: str = "UTC"
    ) -> List[Dict]:
        """List upcoming events from user's calendar"""
        try:
            # Get valid credentials
            creds = self.auth_service.get_credentials(user_id)
            
            # Create Google Calendar API client
            service = build('calendar', 'v3', credentials=creds)
            
            # Call the Calendar API
            now = time_min or datetime.utcnow()
            events_result = service.events().list(
                calendarId='primary',
                timeMin=now.isoformat() + 'Z',  # 'Z' indicates UTC time
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime',
                timeZone=timezone
            ).execute()
            
            events = events_result.get('items', [])
            
            # Format the response
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'No title'),
                    'description': event.get('description', ''),
                    'start': event['start'].get('dateTime', event['start'].get('date')),
                    'end': event['end'].get('dateTime', event['end'].get('date')),
                    'htmlLink': event.get('htmlLink'),
                    'hangoutLink': event.get('hangoutLink'),
                    'status': event.get('status')
                })
                
            return formatted_events
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to fetch events: {str(e)}"
            )

    async def delete_event(self, user_id: str, event_id: str) -> Dict:
        """Delete a calendar event"""
        try:
            # Get valid credentials
            creds = self.auth_service.get_credentials(user_id)
            
            # Create Google Calendar API client
            service = build('calendar', 'v3', credentials=creds)
            
            # Delete the event
            service.events().delete(
                calendarId='primary',
                eventId=event_id,
                sendUpdates='all'
            ).execute()
            
            return {
                'status': 'success',
                'message': 'Event deleted successfully',
                'event_id': event_id
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to delete event: {str(e)}"
            )
