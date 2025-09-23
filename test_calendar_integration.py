import os
import sys
from datetime import datetime, timedelta

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import the modules
from models.database import Base, engine, SessionLocal
from models.oauth_token import OAuthToken
from services.oauth_service import OAuthService
from services.google_calendar import GoogleCalendarService

def setup_database():
    """Set up SQLite database and create tables."""
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    return SessionLocal()

def test_calendar_integration():
    """Test the Google Calendar integration."""
    # Set up database session
    db_session = setup_database()
    
    # Initialize services
    user_id = "test_user_1"
    oauth_service = OAuthService(db_session)
    
    # First, get the authorization URL
    redirect_uri = "http://localhost:8000/oauth2callback"  # Update this with your actual redirect URI
    auth_url = oauth_service.get_authorization_url(user_id, redirect_uri)
    
    print(f"Please visit this URL to authorize the application:\n{auth_url}\n")
    print("After authorizing, you'll be redirected to a URL. Paste that URL below:")
    
    # Get the authorization code from the redirect URL
    redirect_response = input("Enter the full redirect URL: ")
    
    # Extract the authorization code from the redirect URL
    from urllib.parse import urlparse, parse_qs
    parsed = urlparse(redirect_response)
    code = parse_qs(parsed.query).get('code', [None])[0]
    
    if not code:
        print("No authorization code found in the URL.")
        return
    
    # Save the credentials
    if oauth_service.save_credentials(user_id, code, redirect_uri):
        print("\n✅ Successfully authenticated with Google Calendar!")
    else:
        print("\n❌ Failed to authenticate with Google Calendar.")
        return
    
    # Now test creating a calendar event
    try:
        calendar_service = GoogleCalendarService(oauth_service, user_id)
        
        # Create a test event in 1 hour from now
        now = datetime.utcnow()
        start_time = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        end_time = (now + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")
        
        event_config = {
            "summary": "Test Meeting from Python",
            "description": "This is a test event created by the integration.",
            "start_time": start_time,
            "end_time": end_time,
            "attendees": ["your-email@example.com"],  # Replace with actual email
            "timezone": "Asia/Kolkata"
        }
        
        print("\nCreating test event...")
        result = calendar_service.create_meeting(event_config)
        
        print("\n✅ Event created successfully!")
        print(f"Event Link: {result['html_link']}")
        print(f"Meet Link: {result['meet_link']}")
        
        # List upcoming events
        print("\nUpcoming events:")
        events = calendar_service.list_upcoming_events(5)
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"- {start}: {event['summary']}")
            
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    test_calendar_integration()
