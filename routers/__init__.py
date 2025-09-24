from .auth import router as auth_router
from .calendar_router import router as calendar_router
from .testimonials import router as testimonials_router

__all__ = ['auth_router', 'calendar_router', 'testimonials_router']
