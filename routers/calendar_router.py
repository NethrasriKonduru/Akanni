from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from models.user import User
from sqlalchemy.orm import Session
from pydantic import BaseModel
from urllib.parse import urlencode

from database import get_db
from services.calendar_service import CalendarService
from services.google_auth import GoogleAuthService

router = APIRouter(prefix="", tags=["Google Calendar"])

# Request/Response Models
class EventCreate(BaseModel):
    summary: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    attendees: List[str] = []
    timezone: str = "UTC"

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class EventResponse(BaseModel):
    id: str
    htmlLink: Optional[str] = None
    hangoutLink: Optional[str] = None
    start: str
    end: str
    status: str

# Import the auth_utils for proper JWT handling
from auth_utils import get_current_user as get_current_user_from_token

# Helper function to get user ID from JWT token
def get_current_user(
    current_user: User = Depends(get_current_user_from_token)
) -> str:
    """Extract user ID from JWT token"""
    return str(current_user.id)

# OAuth Endpoints
@router.get("/init-oauth")
async def init_google_oauth(
    request: Request,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """Initialize Google OAuth flow"""
    try:
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        redirect_uri = f"{base_url}/api/v1/auth/google/callback"
        
        auth_service = GoogleAuthService(db)
        auth_url = auth_service.get_authorization_url(redirect_uri, user_id)
        return {"authorization_url": auth_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize OAuth: {str(e)}"
        )

# Calendar Endpoints
@router.post("/events/", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Create a new Google Calendar event with Google Meet
    """
    calendar_service = CalendarService(db)
    return await calendar_service.create_event(
        user_id=user_id,
        summary=event.summary,
        description=event.description,
        start_datetime=event.start_datetime,
        end_datetime=event.end_datetime,
        attendees=event.attendees,
        timezone=event.timezone
    )

@router.get("/events/", response_model=List[EventResponse])
async def list_events(
    time_min: Optional[datetime] = None,
    max_results: int = 10,
    timezone: str = "UTC",
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    List upcoming events from user's Google Calendar
    """
    calendar_service = CalendarService(db)
    return await calendar_service.list_events(
        user_id=user_id,
        time_min=time_min,
        max_results=max_results,
        timezone=timezone
    )

@router.delete("/events/{event_id}")
async def delete_event(
    event_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Delete a calendar event
    """
    calendar_service = CalendarService(db)
    return await calendar_service.delete_event(
        user_id=user_id,
        event_id=event_id
    )
