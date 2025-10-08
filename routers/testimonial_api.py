from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
import shutil
from pathlib import Path
import base64
from typing import Optional, Dict, Any

import models
from database import SessionLocal, engine
from models.base import Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/api/v1/testimonials",
    tags=["testimonials"],
    responses={404: {"description": "Not found"}},
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configure upload directories
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
VIDEOS_DIR = UPLOAD_DIR / "videos"
IMAGES_DIR = UPLOAD_DIR / "images"

# Ensure upload directories exist
for directory in [VIDEOS_DIR, IMAGES_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# Pydantic model for request/response
from pydantic import BaseModel

class TestimonialBase(BaseModel):
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    content: str
    rating: Optional[int] = None
    is_featured: bool = False

class TestimonialCreate(TestimonialBase):
    pass

class TestimonialUpdate(TestimonialBase):
    name: Optional[str] = None
    content: Optional[str] = None

class MediaContent(BaseModel):
    filename: str
    content_type: str
    content: str  # base64 encoded content

class TestimonialResponse(TestimonialBase):
    id: int
    image: Optional[MediaContent] = None
    video: Optional[MediaContent] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        result = super().from_orm(obj)

        def get_media_content(file_path: str) -> Optional[Dict[str, Any]]:
            if not file_path:
                print(f"[DEBUG] No file path provided for testimonial {getattr(obj, 'id', 'unknown')}")
                return None
                
            print(f"[DEBUG] Processing media file: {file_path}")
            print(f"[DEBUG] UPLOAD_DIR: {UPLOAD_DIR}")
            print(f"[DEBUG] VIDEOS_DIR: {VIDEOS_DIR}")
            print(f"[DEBUG] IMAGES_DIR: {IMAGES_DIR}")
            
            try:
                # Normalize path separators for Windows
                file_path = file_path.replace('\\', '/')
                
                # Check if the path is already absolute
                if os.path.isabs(file_path):
                    full_path = Path(file_path)
                else:
                    # Try to find the file in the uploads directory
                    full_path = UPLOAD_DIR / file_path
                    
                    # If not found, try to find it in the appropriate subdirectory
                    if not full_path.exists():
                        print(f"[DEBUG] File not found at {full_path}, trying subdirectories...")
                        
                        # Check if it's a video or image based on the path
                        if 'videos' in file_path.lower() or file_path.lower().endswith(('.mp4', '.webm', '.mov')):
                            # Try to find in videos directory
                            full_path = VIDEOS_DIR / Path(file_path).name
                            if not full_path.exists():
                                # Try to find by ID in the videos directory
                                matching_files = list(VIDEOS_DIR.glob(f"{obj.id}_*"))
                                if matching_files:
                                    full_path = matching_files[0]
                                    print(f"[DEBUG] Found video file by ID: {full_path}")
                        else:
                            # Try to find in images directory
                            full_path = IMAGES_DIR / Path(file_path).name
                            if not full_path.exists():
                                # Try to find by ID in the images directory
                                matching_files = list(IMAGES_DIR.glob(f"{obj.id}_*"))
                                if matching_files:
                                    full_path = matching_files[0]
                                    print(f"[DEBUG] Found image file by ID: {full_path}")
                    
                    # If still not found, try to find the file anywhere in the uploads directory
                    if not full_path.exists():
                        print(f"[DEBUG] File not found at {full_path}, searching in uploads directory...")
                        matching_files = list(UPLOAD_DIR.rglob(Path(file_path).name))
                        if matching_files:
                            full_path = matching_files[0]
                            print(f"[DEBUG] Found file at: {full_path}")
                        else:
                            # As a last resort, try to find any file with the same name in any subdirectory (case-insensitive)
                            for root, dirs, files in os.walk(UPLOAD_DIR):
                                for file in files:
                                    if file.lower() == Path(file_path).name.lower():
                                        full_path = Path(root) / file
                                        print(f"[DEBUG] Found matching file (case-insensitive): {full_path}")
                                        break
                
                print(f"[DEBUG] Final file path being checked: {full_path}")
                
                if not full_path.exists():
                    print(f"[DEBUG] File not found at path: {full_path}")
                    print(f"[DEBUG] Current working directory: {os.getcwd()}")
                    print(f"[DEBUG] UPLOAD_DIR exists: {UPLOAD_DIR.exists()}")
                    print(f"[DEBUG] VIDEOS_DIR exists: {VIDEOS_DIR.exists() if VIDEOS_DIR.exists() else 'No'}")
                    print(f"[DEBUG] IMAGES_DIR exists: {IMAGES_DIR.exists() if IMAGES_DIR.exists() else 'No'}")
                    # Return a helpful error message instead of None
                    return {
                        'filename': Path(file_path).name,
                        'content_type': 'application/octet-stream',
                        'content': '',
                        'error': f'File not found at {full_path}',
                        'path': str(full_path),
                        'original_path': file_path
                    }

                ext = full_path.suffix.lower()
                print(f"[DEBUG] File extension: {ext}")
                
                content_type = {
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.png': 'image/png',
                    '.gif': 'image/gif',
                    '.mp4': 'video/mp4',
                    '.webm': 'video/webm',
                    '.mov': 'video/quicktime'
                }.get(ext, 'application/octet-stream')
                
                print(f"[DEBUG] Content type: {content_type}")

                with open(full_path, 'rb') as f:
                    content = base64.b64encode(f.read()).decode('utf-8')
                    print(f"[DEBUG] Successfully read {len(content)} bytes from {full_path}")

                return {
                    'filename': full_path.name,
                    'content_type': content_type,
                    'content': content
                }

            except Exception as e:
                import traceback
                error_msg = f"Error processing file {file_path}: {str(e)}"
                print(f"[ERROR] {error_msg}")
                print(traceback.format_exc())
                return {
                    'filename': Path(file_path).name if file_path else 'unknown',
                    'content_type': 'application/octet-stream',
                    'content': '',
                    'error': error_msg,
                    'traceback': traceback.format_exc()
                }

        # Process image and video paths with debug info
        if hasattr(obj, 'image_path') and obj.image_path:
            print(f"[DEBUG] Processing image path: {obj.image_path}")
            result.image = get_media_content(obj.image_path)
            print(f"[DEBUG] Image result: {result.image is not None}")
            
        if hasattr(obj, 'video_path') and obj.video_path:
            print(f"[DEBUG] Processing video path: {obj.video_path}")
            result.video = get_media_content(obj.video_path)
            print(f"[DEBUG] Video result: {result.video is not None}")
            if result.video and 'error' in result.video:
                print(f"[DEBUG] Video error: {result.video['error']}")

        return result
# Helper function to save uploaded file
def save_upload_file(upload_file: UploadFile, directory: Path, file_id: int) -> str:
    print(f"[DEBUG] save_upload_file called with file: {upload_file.filename}, directory: {directory}, id: {file_id}")
    
    # Create directory if it doesn't exist
    directory.mkdir(parents=True, exist_ok=True)
    print(f"[DEBUG] Directory ensured: {directory}")
    
    # Get current timestamp in YYYYMMDD_HHMMSS format
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a safe filename using the testimonial ID and timestamp
    file_ext = Path(upload_file.filename).suffix.lower()
    file_name = f"{file_id}_{timestamp}{file_ext}"
    file_path = directory / file_name
    
    print(f"[DEBUG] Saving file to: {file_path.absolute()}")
    
    try:
        # Save the file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        # Verify the file was saved
        if not file_path.exists():
            raise Exception(f"File was not created at {file_path}")
            
        # Get the relative path from UPLOAD_DIR
        relative_path = str(file_path.relative_to(UPLOAD_DIR))
        print(f"[DEBUG] File saved successfully: {file_path.absolute()}")
        print(f"[DEBUG] Relative path: {relative_path}")
        print(f"[DEBUG] File size: {file_path.stat().st_size} bytes")
        
        return relative_path
        
    except Exception as e:
        print(f"[ERROR] Error saving file {file_path}: {str(e)}")
        # Print the current working directory for debugging
        print(f"[DEBUG] Current working directory: {os.getcwd()}")
        print(f"[DEBUG] Directory exists: {directory.exists()}")
        print(f"[DEBUG] Directory is writable: {os.access(directory, os.W_OK)}")
        raise

# CRUD Endpoints
@router.post("/", response_model=TestimonialResponse, status_code=status.HTTP_201_CREATED)
async def create_testimonial(
    name: str = Form(...),
    role: str = Form(None),
    company: str = Form(None),
    content: str = Form(...),
    rating: int = Form(None),
    is_featured: bool = Form(False),
    image: UploadFile = File(None),
    video: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    print("[DEBUG] ===== Starting testimonial creation =====")
    print(f"[DEBUG] Received video file: {video.filename if video else 'None'}")
    
    try:
        # Start a transaction
        db_testimonial = None
        try:
            # Create the testimonial first to get an ID
            db_testimonial = models.Testimonial(
                name=name,
                role=role,
                company=company,
                content=content,
                rating=rating,
                is_featured=is_featured
            )
            
            db.add(db_testimonial)
            db.flush()  # Flush to get the ID without committing
            print(f"[DEBUG] Created testimonial with ID: {db_testimonial.id}")
            
            # Handle image upload
            if image:
                print("[DEBUG] Processing image upload")
                try:
                    db_testimonial.image_path = save_upload_file(image, IMAGES_DIR, db_testimonial.id)
                    print(f"[DEBUG] Image saved to: {db_testimonial.image_path}")
                    db.flush()
                except Exception as img_err:
                    print(f"[ERROR] Error saving image: {str(img_err)}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error saving image: {str(img_err)}"
                    )
            
            # Handle video upload
            if video:
                print("[DEBUG] Processing video upload")
                try:
                    db_testimonial.video_path = save_upload_file(video, VIDEOS_DIR, db_testimonial.id)
                    print(f"[DEBUG] Video saved to: {db_testimonial.video_path}")
                    db.flush()
                except Exception as vid_err:
                    print(f"[ERROR] Error saving video: {str(vid_err)}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error saving video: {str(vid_err)}"
                    )
            
            # Commit the transaction
            db.commit()
            print("[DEBUG] Transaction committed successfully")
            
            # Refresh the object to get all the latest data
            db.refresh(db_testimonial)
            print("[DEBUG] Refreshed testimonial object")
            
            # Convert to response model
            response = TestimonialResponse.from_orm(db_testimonial)
            print("[DEBUG] Converted to response model")
            print(f"[DEBUG] Response contains video: {response.video is not None}")
            
            return response
            
        except Exception as e:
            db.rollback()
            print(f"[ERROR] Error in transaction: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating testimonial: {str(e)}"
            )
            
    except Exception as e:
        print(f"[ERROR] Error in testimonial creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

@router.get("/", response_model=List[TestimonialResponse])
def read_testimonials(
    skip: int = 0, 
    limit: int = 100, 
    featured: bool = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Testimonial)
    if featured is not None:
        query = query.filter(models.Testimonial.is_featured == featured)
    testimonials = query.offset(skip).limit(limit).all()
    return [TestimonialResponse.from_orm(t) for t in testimonials]

@router.get("/{testimonial_id}", response_model=TestimonialResponse)
def read_testimonial(testimonial_id: int, db: Session = Depends(get_db)):
    db_testimonial = db.query(models.Testimonial).filter(models.Testimonial.id == testimonial_id).first()
    if db_testimonial is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return TestimonialResponse.from_orm(db_testimonial)

@router.put("/{testimonial_id}", response_model=TestimonialResponse)
async def update_testimonial(
    testimonial_id: int,
    name: str = Form(None),
    role: str = Form(None),
    company: str = Form(None),
    content: str = Form(None),
    rating: int = Form(None),
    is_featured: bool = Form(None),
    image: UploadFile = File(None),
    video: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        # Start a transaction
        db.begin()
        
        db_testimonial = db.query(models.Testimonial).filter(models.Testimonial.id == testimonial_id).first()
        if db_testimonial is None:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        
        # Update fields if provided
        if name is not None:
            db_testimonial.name = name
        if role is not None:
            db_testimonial.role = role
        if company is not None:
            db_testimonial.company = company
        if content is not None:
            db_testimonial.content = content
        if rating is not None:
            db_testimonial.rating = rating
        if is_featured is not None:
            db_testimonial.is_featured = is_featured
        
        # Handle image upload
        if image:
            print("[DEBUG] Processing image update")
            # Delete old image if exists
            if db_testimonial.image_path:
                old_image = UPLOAD_DIR / db_testimonial.image_path
                if old_image.exists():
                    old_image.unlink()
            db_testimonial.image_path = save_upload_file(image, IMAGES_DIR, db_testimonial.id)
            db.flush()

        # Handle video upload
        if video:
            print("[DEBUG] Processing video update")
            # Delete old video if exists
            if db_testimonial.video_path:
                old_video = UPLOAD_DIR / db_testimonial.video_path
                if old_video.exists():
                    old_video.unlink()
            db_testimonial.video_path = save_upload_file(video, VIDEOS_DIR, db_testimonial.id)
            db.flush()
        
        # Update the timestamp
        db_testimonial.updated_at = datetime.utcnow()
        
        # Commit the transaction
        db.commit()
        
        # Refresh to get the latest data
        db.refresh(db_testimonial)
        
        # Convert to response model
        return TestimonialResponse.from_orm(db_testimonial)
        
    except Exception as e:
        print(f"[ERROR] Error updating testimonial: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating testimonial: {str(e)}"
        )

@router.delete("/{testimonial_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_testimonial(testimonial_id: int, db: Session = Depends(get_db)):
    db_testimonial = db.query(models.Testimonial).filter(models.Testimonial.id == testimonial_id).first()
    if db_testimonial is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    # Delete associated files
    if db_testimonial.image_path:
        image_path = UPLOAD_DIR / db_testimonial.image_path
        if image_path.exists():
            image_path.unlink()
    
    if db_testimonial.video_path:
        video_path = UPLOAD_DIR / db_testimonial.video_path
        if video_path.exists():
            video_path.unlink()
    
    # Delete from database
    db.delete(db_testimonial)
    db.commit()
    return None
