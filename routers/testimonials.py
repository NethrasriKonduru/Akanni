import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Optional
from pathlib import Path
from pydantic import BaseModel

# API router for media endpoints
api_router = APIRouter(prefix="/media", tags=["Media"])

# Web UI router
web_router = APIRouter(tags=["Web UI"])

@web_router.get("/testimonials", response_class=HTMLResponse)
async def get_testimonials_page(request: Request):
    """Serve the testimonials HTML page"""
    return templates.TemplateResponse(
        "testimonials.html",
        {"request": request, "title": "Testimonials"}
    )

# Main router for the application
router = APIRouter()
router.include_router(api_router)
router.include_router(web_router)

templates = Jinja2Templates(directory="testimonials")

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PICTURES_DIR = os.path.join(BASE_DIR, "testimonials", "pictures")
VIDEOS_DIR = os.path.join(BASE_DIR, "testimonials", "video")

# Supported file extensions
PICTURE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.webm', '.avi', '.mkv'}

class MediaItem(BaseModel):
    name: str
    type: str  # 'picture' or 'video'
    path: str

def get_media_files() -> Dict[str, List[MediaItem]]:
    """Get all media files from both pictures and videos directories."""
    media = {"pictures": [], "videos": []}
    
    # Ensure directories exist
    os.makedirs(PICTURES_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    
    print(f"Pictures directory: {PICTURES_DIR}")
    print(f"Videos directory: {VIDEOS_DIR}")
    
    # Get picture files
    try:
        picture_files = os.listdir(PICTURES_DIR)
        print(f"Found {len(picture_files)} files in pictures directory")
        for filename in picture_files:
            file_ext = os.path.splitext(filename)[1].lower()
            print(f"Checking file: {filename}, extension: {file_ext}")
            if file_ext in PICTURE_EXTENSIONS:
                media["pictures"].append(MediaItem(
                    name=filename,
                    type="picture",
                    path=f"pictures/{filename}"
                ))
    except Exception as e:
        print(f"Error reading pictures directory: {e}")
    
    # Get video files
    try:
        video_files = os.listdir(VIDEOS_DIR)
        print(f"Found {len(video_files)} files in videos directory")
        for filename in video_files:
            file_ext = os.path.splitext(filename)[1].lower()
            print(f"Checking file: {filename}, extension: {file_ext}")
            if file_ext in VIDEO_EXTENSIONS:
                media["videos"].append(MediaItem(
                    name=filename,
                    type="video",
                    path=f"video/{filename}"
                ))
    except Exception as e:
        print(f"Error reading videos directory: {e}")
    
    print(f"Found {len(media['pictures'])} pictures and {len(media['videos'])} videos")
    return media

@api_router.get("/media/all", response_model=List[Dict[str, str]])
async def list_all_media():
    """Get a combined list of all media files (both images and videos)."""
    media = get_media_files()
    all_media = []
    
    # Add type information and convert to a simpler format
    for media_item in media["pictures"]:
        all_media.append({
            "name": media_item.name,
            "type": "image",
            "url": f"/api/v1/media/pictures/{media_item.name}",
            "thumbnail": f"/api/v1/media/pictures/{media_item.name}"  # In a real app, you might want to generate thumbnails
        })
    
    for media_item in media["videos"]:
        all_media.append({
            "name": media_item.name,
            "type": "video",
            "url": f"/api/v1/media/videos/{media_item.name}",
            "thumbnail": "/path/to/video/thumbnail.jpg"  # You would need to implement thumbnail generation
        })
    
    return all_media

@api_router.get("/media", response_model=Dict[str, List[MediaItem]])
async def list_media():
    """List all available media files (both pictures and videos)."""
    return get_media_files()

@api_router.get("/pictures/", response_model=List[MediaItem])
async def list_pictures():
    """List all available picture files."""
    return get_media_files()["pictures"]

@api_router.get("/videos/", response_model=List[MediaItem])
async def list_videos():
    """List all available media files (both photos and videos)."""
    media = get_media_files()
    # Combine both photos and videos into a single list
    return media["pictures"] + media["videos"]

@api_router.get("/pictures/{filename}")
async def get_picture(filename: str):
    """Get a specific picture file by filename."""
    return serve_media_file(filename, PICTURES_DIR, PICTURE_EXTENSIONS)

@api_router.get("/videos/{filename}")
async def get_video(filename: str, request: Request):
    """Get a specific video file by filename with support for range requests."""
    # Security check to prevent directory traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Check file extension
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in VIDEO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported video format")
    
    file_path = os.path.join(VIDEOS_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Get file size for range requests
    file_size = os.path.getsize(file_path)
    
    # Handle range requests for video streaming
    range_header = request.headers.get('Range')
    if range_header:
        # Parse the range header (e.g., 'bytes=0-' or 'bytes=0-999')
        start_byte, end_byte = 0, None
        range_units = range_header.replace('bytes=', '').split('-')
        if range_units[0]:
            start_byte = int(range_units[0])
        if len(range_units) > 1 and range_units[1]:
            end_byte = int(range_units[1])
        else:
            end_byte = file_size - 1
        
        # Set content length for the range
        content_length = end_byte - start_byte + 1
        
        # Create a file-like object for the range
        file = open(file_path, 'rb')
        file.seek(start_byte)
        data = file.read(content_length)
        file.close()
        
        # Create a response with the partial content
        response = Response(
            content=data,
            status_code=206,  # Partial Content
            media_type=get_media_type(file_ext),
            headers={
                'Accept-Ranges': 'bytes',
                'Content-Range': f'bytes {start_byte}-{end_byte}/{file_size}',
                'Content-Length': str(content_length),
                'Content-Disposition': f'inline; filename="{filename}"'
            }
        )
        return response
    
    # If no range header, serve the whole file
    return FileResponse(
        file_path,
        media_type=get_media_type(file_ext),
        filename=filename,
        headers={
            'Accept-Ranges': 'bytes',
            'Content-Length': str(file_size),
            'Content-Disposition': f'inline; filename="{filename}"'
        }
    )

@web_router.get("/videos/", response_class=HTMLResponse)
async def list_videos_page(request: Request):
    """Serve the videos listing page."""
    media = get_media_files()
    return templates.TemplateResponse(
        "video_list.html",
        {"request": request, "videos": media["videos"]}
    )

@web_router.get("/videos/play/{filename}", response_class=HTMLResponse)
async def play_video(request: Request, filename: str):
    """Serve the video player page for a specific video."""
    # Verify the file exists and is a video
    file_path = os.path.join(VIDEOS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in VIDEO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File is not a supported video format")
    
    video_url = f"/api/v1/media/videos/{filename}"
    return templates.TemplateResponse(
        "video_player.html",
        {"request": request, "video_url": video_url}
    )

def serve_media_file(filename: str, base_dir: str, allowed_extensions: set, stream: bool = False):
    """Helper function to serve media files with security checks."""
    # Security check to prevent directory traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Check file extension
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    file_path = os.path.join(base_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Use streaming for large files like videos
    return FileResponse(file_path, media_type=get_media_type(file_ext), filename=filename)

def get_media_type(extension: str) -> str:
    """Get the appropriate media type for the given file extension."""
    extension = extension.lower()
    if extension == '.jpg' or extension == '.jpeg':
        return 'image/jpeg'
    elif extension == '.png':
        return 'image/png'
    elif extension == '.gif':
        return 'image/gif'
    elif extension == '.webp':
        return 'image/webp'
    elif extension == '.mp4':
        return 'video/mp4'
    elif extension == '.webm':
        return 'video/webm'
    elif extension in {'.mov', '.avi', '.mkv'}:
        return 'video/*'
    return 'application/octet-stream'

# Export the main router
router = APIRouter()
router.include_router(api_router, prefix="/media", tags=["Media"])
router.include_router(web_router, tags=["Web UI"])