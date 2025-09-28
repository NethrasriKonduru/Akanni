from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from urllib.parse import urlencode
from datetime import datetime, timedelta

from database import get_db
from services.oauth_service import OAuthService
from models.user import User
from schemas.auth import UserCreate, UserInDB, UserLogin, Token
from auth_utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

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

@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        user: User registration data including email, full_name, and password
        db: Database session
        
    Returns:
        UserInDB: The created user object
        
    Raises:
        HTTPException: If email is already registered
    """
    # Check if user with this email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.utcnow()
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login_user(
    creds: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with email and password, return JWT access token.
    """
    user = db.query(User).filter(User.email == creds.email).first()
    if not user or not user.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not verify_password(creds.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"}

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
