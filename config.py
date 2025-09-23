import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Google OAuth2 credentials from JSON file
def load_google_oauth_config():
    config_path = Path(__file__).parent / "config" / "google_oauth.json"
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            "Google OAuth configuration file not found. "
            f"Please create {config_path} with your Google OAuth credentials."
        )

# Load Google OAuth configuration
GOOGLE_CLIENT_CONFIG = load_google_oauth_config()

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
