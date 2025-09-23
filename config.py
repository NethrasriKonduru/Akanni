import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google OAuth2 credentials
GOOGLE_CLIENT_CONFIG = {
    "web": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost:8000/auth/google/callback"]
    }
}

# Email configuration
EMAIL_CONFIG = {
    "SMTP_SERVER": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "SMTP_PORT": int(os.getenv("SMTP_PORT", 587)),
    "SMTP_USERNAME": os.getenv("SMTP_USERNAME"),
    "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD"),
    "FROM_EMAIL": os.getenv("FROM_EMAIL"),
    "FROM_NAME": os.getenv("FROM_NAME", "Department Services")
}

# Scopes for Google Calendar API
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

# Path to store token
BASE_DIR = Path(__file__).parent
TOKEN_PATH = BASE_DIR / "token.json"
CREDENTIALS_PATH = BASE_DIR / "credentials.json"

# Meeting configuration
MEETING_CONFIG = {
    "conferenceDataVersion": 1,
    "sendUpdates": "all",
}
