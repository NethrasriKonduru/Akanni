# Department Services API with Google Meet Integration

This API allows you to manage departments, services, and schedule Google Meet meetings with automatic email invitations.

## Features

- Manage departments and services
- Schedule Google Meet meetings
- Send email invitations to attendees
- View meeting details
- RESTful API with OpenAPI documentation

## Prerequisites

- Python 3.7+
- MySQL Server
- Google Cloud Platform account with Calendar API enabled
- Gmail account for sending emails

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Akkani
   ```

2. **Create a virtual environment and activate it**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the `.env` file with your configuration:
     - Database credentials
     - Google OAuth credentials
     - Email server settings

5. **Set up Google OAuth**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials (Web application)
   - Add `http://localhost:8000/auth/google/callback` as an authorized redirect URI
   - Download the credentials JSON and save it as `credentials.json` in the project root

6. **Initialize the database**
   ```bash
   python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication

1. When you first access the API, you'll be redirected to Google for authentication
2. After authenticating, you'll be redirected back to the application
3. The OAuth token will be stored in `token.json`

## Usage Examples

### Schedule a Meeting

```http
POST /api/v1/schedule-meeting/
Content-Type: application/json

{
  "title": "Team Sync",
  "description": "Weekly team sync meeting",
  "start_time": "2023-01-01T10:00:00",
  "end_time": "2023-01-01T11:00:00",
  "attendees": ["attendee1@example.com", "attendee2@example.com"],
  "organizer_email": "organizer@example.com",
  "organizer_name": "John Doe"
}
```

### Get Meeting Details

```http
GET /api/v1/meeting/{meeting_id}
```

## Troubleshooting

- If you get authentication errors, delete the `token.json` file and restart the application
- Make sure the Google Calendar API is enabled in your Google Cloud Console
- Ensure all required environment variables are properly set in the `.env` file
- Check the console logs for detailed error messages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
