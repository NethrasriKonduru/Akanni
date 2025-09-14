import os
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import GOOGLE_CLIENT_CONFIG, SCOPES, TOKEN_PATH, CREDENTIALS_PATH, MEETING_CONFIG

class GoogleCalendar:
    def __init__(self):
        self.creds = self._get_credentials()
        self.service = build('calendar', 'v3', credentials=self.creds)

    def _get_credentials(self):
        creds = None
        
        # Load token if it exists
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
        # If there are no (valid) credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Create credentials.json if it doesn't exist
                if not os.path.exists(CREDENTIALS_PATH):
                    with open(CREDENTIALS_PATH, 'w') as f:
                        json.dump(GOOGLE_CLIENT_CONFIG, f)
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        
        return creds

    def create_meeting(self, summary, start_time, end_time, attendees_emails, description=""):
        """
        Create a Google Meet event and return the meeting details
        
        Args:
            summary (str): Meeting title
            start_time (datetime): Start time of the meeting
            end_time (datetime): End time of the meeting
            attendees_emails (list): List of email addresses to invite
            description (str): Meeting description (optional)
            
        Returns:
            dict: Meeting details including join URL
        """
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'attendees': [{'email': email} for email in attendees_emails],
            'conferenceData': {
                'createRequest': {
                    'requestId': f"sample123{datetime.utcnow().isoformat()}",
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                }
            },
            'reminders': {
                'useDefault': True,
            },
        }
        
        # Create the event with Google Meet
        event = self.service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=MEETING_CONFIG['conferenceDataVersion'],
            sendUpdates=MEETING_CONFIG['sendUpdates']
        ).execute()
        
        # Extract meeting details
        meeting_details = {
            'meeting_id': event.get('id'),
            'summary': event.get('summary'),
            'start_time': event['start'].get('dateTime', event['start'].get('date')),
            'end_time': event['end'].get('dateTime', event['end'].get('date')),
            'hangout_link': event.get('hangoutLink', ''),
            'meet_link': event.get('hangoutLink', ''),
            'html_link': event.get('htmlLink', ''),
            'attendees': [attendee.get('email') for attendee in event.get('attendees', [])],
            'status': event.get('status'),
            'created': event.get('created'),
            'updated': event.get('updated')
        }
        
        return meeting_details
