# This file aggregates all your FastAPI routers for easy import in main.py

from .auth import router as auth_router
from .calendar import router as calendar_router

# FIX: Changed 'main_router' to 'router' to match the variable name in testimonials.py
from .testimonials import router as testimonials_router 

# You can now import all three from 'from routers import ...' in main.py
__all__ = ["auth_router", "calendar_router", "testimonials_router"]
