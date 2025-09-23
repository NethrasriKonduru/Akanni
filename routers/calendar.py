from fastapi import APIRouter, HTTPException, Depends, Request, status, Header
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from pydantic import BaseModel
from database import get_db
from sqlalchemy.orm import Session
from services.oauth_service import OAuthService, CalendarService
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

router = APIRouter(prefix="/api/v1/calendar", tags=["Google Calendar"])

class EventCreate(BaseModel):
    summary: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    timezone: str = "Asia/Kolkata"
    attendees: Optional[List[str]] = None

class EventResponse(BaseModel):
    id: str
    htmlLink: str
    summary: str
    description: str
    start: datetime
    end: datetime
    attendees: List[Dict[str, str]]
    hangoutLink: Optional[str] = None

def get_current_user_id(authorization: str = Header(...)) -> str:
    """
    Extract user ID from Authorization header
    In a real application, you would validate the JWT token here
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    # In a real app, you would decode the JWT token here
    # and return the user ID from the token
    # For now, we'll just return the token as the user ID
    return authorization.replace("Bearer ", "")

def get_calendar_service(user_id: str, db: Session) -> CalendarService:
    """
    Get an instance of CalendarService for the current user
    """
    oauth_service = OAuthService(db)
    return CalendarService(oauth_service, db)

@router.post("/events/", response_model=EventResponse)
async def create_calendar_event(
    event: EventCreate,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Create a new Google Calendar event with a Google Meet link
    """
    try:
        user_id = get_current_user_id(authorization)
        calendar_service = get_calendar_service(user_id, db)
        
        # Create the event
        event_result = calendar_service.create_meet_event(
            user_id=user_id,
            summary=event.summary,
            start_time=event.start_datetime,
            end_time=event.end_datetime,
            attendees=event.attendees or []
        )
        
        return event_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create event: {str(e)}"
        )

@router.get("/upcoming/", response_model=List[EventResponse])
async def get_upcoming_events(
    start_date: Optional[datetime] = None,
    max_results: int = 10,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Get upcoming events from Google Calendar
    """
    try:
        user_id = get_current_user_id(authorization)
        oauth_service = OAuthService(db)
        
        # Get user's credentials
        token = oauth_service.get_token(user_id)
        if not token or not token.credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User has not connected Google Calendar"
            )
            
        # Create Google Calendar service
        creds = Credentials.from_authorized_user_info(
            json.loads(token.credentials),
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        
        service = build('calendar', 'v3', credentials=creds)
        
        # Call the Calendar API
        now = start_date or datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Format the response
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            formatted_events.append({
                'id': event['id'],
                'htmlLink': event.get('htmlLink', ''),
                'summary': event.get('summary', 'No title'),
                'description': event.get('description', ''),
                'start': start,
                'end': end,
                'attendees': [{'email': a['email']} for a in event.get('attendees', [])],
                'hangoutLink': event.get('hangoutLink')
            })
            
        return formatted_events
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch events: {str(e)}"
        )

@router.delete("/events/{event_id}")
async def remove_calendar_event(
    event_id: str,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Delete a Google Calendar event
    """
    try:
        user_id = get_current_user_id(authorization)
        oauth_service = OAuthService(db)
        
        # Get user's credentials
        token = oauth_service.get_token(user_id)
        if not token or not token.credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User has not connected Google Calendar"
            )
            
        # Create Google Calendar service
        creds = Credentials.from_authorized_user_info(
            json.loads(token.credentials),
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        
        service = build('calendar', 'v3', credentials=creds)
        
        # Delete the event
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        
        return {
            "status": "success",
            "message": "Event deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete event: {str(e)}"
        )
