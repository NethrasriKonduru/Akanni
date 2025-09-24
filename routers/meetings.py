from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# from google_calendar import GoogleCalendar
from email_service import EmailService
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class MeetingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    attendees: List[str]
    organizer_email: str
    organizer_name: Optional[str] = None

@router.post("/schedule-meeting/")
async def schedule_meeting(meeting: MeetingCreate, db: Session = Depends(get_db)):
    """
    Schedule a new Google Meet meeting and send invitations
    """
    try:
        # Google Calendar integration is currently disabled
        # calendar = GoogleCalendar()
        # meeting_details = calendar.create_meeting(
        #     summary=meeting.title,
        #     description=meeting.description or "",
        #     start_time=meeting.start_time,
        #     end_time=meeting.end_time,
        #     attendees_emails=meeting.attendees
        # )
        
        # Create a placeholder response
        meeting_details = {
            "id": "local_meeting_" + str(hash(meeting.title + str(meeting.start_time))),
            "summary": meeting.title,
            "description": meeting.description or "",
            "start": {"dateTime": meeting.start_time.isoformat()},
            "end": {"dateTime": meeting.end_time.isoformat()},
            "hangoutLink": "#google-calendar-disabled",
            "status": "confirmed"
        }
        
        # Add meeting link to the details
        meeting_details['meet_link'] = meeting_details.get('hangoutLink', '')
        
        # Send email invitations
        email_service = EmailService()
        email_service.send_meeting_invitation(
            to_emails=meeting.attendees,
            meeting_details={
                'summary': meeting.title,
                'start_time': meeting.start_time.strftime("%Y-%m-%d %H:%M"),
                'end_time': meeting.end_time.strftime("%Y-%m-%d %H:%M"),
                'description': meeting.description or "",
                'meet_link': meeting_details.get('meet_link', '')
            },
            organizer_name=meeting.organizer_name or "Meeting Organizer"
        )
        
        return {
            "status": "success",
            "message": "Meeting scheduled and invitations sent successfully",
            "meeting_details": meeting_details
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule meeting: {str(e)}")

@router.get("/meeting/{meeting_id}")
async def get_meeting(meeting_id: str):
    """
    Get meeting details by ID
    """
    try:
        # Google Calendar integration is currently disabled
        # calendar = GoogleCalendar()
        # event = calendar.service.events().get(
        #     calendarId='primary',
        #     eventId=meeting_id,
        # ).execute()
        # 
        # if not event:
        #     raise HTTPException(status_code=404, detail="Meeting not found")
        #     
        # return event
        
        # Return a placeholder response
        return {
            "id": meeting_id,
            "summary": "Google Calendar Integration Disabled",
            "description": "This feature is currently disabled",
            "status": "tentative",
            "htmlLink": "#google-calendar-disabled"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get meeting details: {str(e)}")
