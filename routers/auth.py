from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
from urllib.parse import urlencode

from database import get_db
from services.oauth_service import OAuthService

router = APIRouter(tags=["Authentication"])

@router.get("/google/login")
async def login(
    request: Request,
    user_id: str = "test_user",  # Default test user, replace with actual user auth
    db: Session = Depends(get_db)
):
    """
    Start the OAuth flow by redirecting to Google's OAuth 2.0 server.
    
    Args:
        request: The FastAPI request object
        user_id: User ID (in a real app, get this from the authenticated session)
        db: Database session
    
    Returns:
        JSON with authorization_url to redirect the user to Google's consent screen
    """
    try:
        # Get the base URL
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        redirect_uri = f"{base_url}/api/v1/google/callback"
        
        # Create OAuth service and get authorization URL
        oauth_service = OAuthService(db)
        auth_url = oauth_service.get_authorization_url(redirect_uri, user_id)
        
        # Return the URL for the frontend to redirect to
        return {"authorization_url": auth_url}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error initiating OAuth flow: {str(e)}"
        )

@router.get("/google/callback")
async def callback(
    request: Request,
    code: str,
    state: str,  # This contains our user_id
    db: Session = Depends(get_db)
):
    """
    Handle the OAuth callback from Google.
    """
    try:
        # Get the base URL from the request
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        redirect_uri = f"{base_url}/api/v1/google/callback"
        
        # Save the credentials
        oauth_service = OAuthService(db)
        success = oauth_service.save_credentials(state, code, redirect_uri)
        
        if success:
            # Redirect to a success page or back to the app
            return RedirectResponse(url=f"{base_url}/calendar/success")
        else:
            return RedirectResponse(url=f"{base_url}/calendar/error?message=auth_failed")
            
    except Exception as e:
        print(f"Error in OAuth callback: {str(e)}")
        return RedirectResponse(url=f"{base_url}/calendar/error?message=server_error")

@router.get("/google/revoke")
async def revoke(
    user_id: str,  # In a real app, you'd get this from the authenticated session
    db: Session = Depends(get_db)
):
    """
    Revoke the user's OAuth token and remove it from the database.
    """
    oauth_service = OAuthService(db)
    success = oauth_service.revoke_token(user_id)
    
    if success:
        return {"status": "success", "message": "Successfully disconnected from Google Calendar"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to revoke token"
        )

@router.get("/status")
async def auth_status(
    user_id: str,  # In a real app, you'd get this from the authenticated session
    db: Session = Depends(get_db)
):
    """
    Check if the user has connected their Google Calendar.
    """
    oauth_service = OAuthService(db)
    creds = oauth_service.get_credentials(user_id)
    
    return {
        "connected": creds is not None,
        "expired": creds.expired if creds else None,
        "client_id": creds.client_id if creds else None
    }
