import os
import sys
import logging
import webbrowser
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    try:
        from models.database import Base, engine, SessionLocal
        from models.oauth_token import OAuthToken
        from services.oauth_service import OAuthService
        from services.google_calendar import GoogleCalendarService
        
        logger.info("All imports successful!")
        
        # Initialize database
        Base.metadata.create_all(bind=engine)
        db_session = SessionLocal()
        
        # Initialize OAuth Service
        user_id = "test_user_1"
        oauth_service = OAuthService(db_session)
        
        # Check if we already have valid credentials
        creds = oauth_service.get_credentials(user_id)
        
        if not creds:
            logger.info("No valid credentials found. Starting OAuth flow...")
            
            # Get the authorization URL
            # Using localhost for testing
            redirect_uri = "http://localhost:8080/"
            auth_url = oauth_service.get_authorization_url(user_id, redirect_uri)
            
            logger.info(f"\nPlease visit this URL to authorize the application:")
            logger.info(auth_url)
            logger.info("\nAfter authorizing, you'll be redirected to a URL. Paste that URL below:")
            
            print("\n1. A browser window should open asking you to sign in to your Google account")
            print("2. After signing in, you'll be redirected to localhost:8080")
            print("3. Copy the ENTIRE URL from your browser's address bar and paste it below")
            print("   It should look like: http://localhost:8080/?state=...&code=...&scope=...")
            
            # Open the browser for the user
            webbrowser.open(auth_url)
            
            # Get the full redirect URL from the user
            redirect_url = input("\nPaste the full redirect URL here: ").strip()
            
            # Parse the authorization code from the URL
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(redirect_url)
            auth_code = parse_qs(parsed.query).get('code', [None])[0]
            
            if not auth_code:
                logger.error("No authorization code found in the URL. Please try again.")
                return
            
            # Save the credentials
            if oauth_service.save_credentials(user_id, auth_code, redirect_uri):
                logger.info("✅ Successfully authenticated with Google Calendar!")
            else:
                logger.error("❌ Failed to authenticate with Google Calendar.")
                return
        
        # Now initialize the Google Calendar service
        logger.info("Initializing Google Calendar service...")
        calendar_service = GoogleCalendarService(oauth_service, user_id)
        
        # Test creating an event
        now = datetime.utcnow()
        start_time = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        end_time = (now + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")
        
        event_config = {
            "summary": "Test Meeting from Python Script",
            "description": "This is a test event created by the integration.",
            "start_time": start_time,
            "end_time": end_time,
            "timezone": "Asia/Kolkata",
            "attendees": ["your-email@example.com"]  # Replace with actual email
        }
        
        logger.info("\nCreating test event...")
        result = calendar_service.create_meeting(event_config)
        
        logger.info("\n✅ Event created successfully!")
        print(f"\nEvent Link: {result['html_link']}")
        print(f"Meet Link: {result['meet_link']}")
        
        # List upcoming events
        print("\nUpcoming events:")
        try:
            events = calendar_service.list_upcoming_events(5)
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"- {start}: {event['summary']}")
        except Exception as e:
            logger.error(f"Error listing events: {e}")
    
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Current sys.path: %s", sys.path)
        logger.error("Current working directory: %s", os.getcwd())
    
    except Exception as e:
        logger.exception("An error occurred:")
    
    finally:
        if 'db_session' in locals():
            db_session.close()
        logger.info("Test completed.")

if __name__ == "__main__":
    main()
