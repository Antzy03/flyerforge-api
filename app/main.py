"""
FlyerForge API - AI-Powered Flyer & Poster Generation

A FastAPI application for generating professional marketing flyers
using AI image generation. Built for RapidAPI marketplace.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .routers import flyers_router


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
## FlyerForge API

Generate stunning marketing flyers and posters for your business using AI.

### Features
- 🎨 Multiple design styles (modern, corporate, playful, etc.)
- 📐 Various sizes for social media and print
- 🎯 Customizable with your brand colors
- ⚡ Fast generation powered by AI

### Quick Start
1. Call `POST /api/v1/flyers/generate` with your business info
2. Get back a URL to your generated flyer
3. Download and use!
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def rapidapi_middleware(request: Request, call_next):
    """
    Middleware to handle RapidAPI headers.
    RapidAPI sends authentication via X-RapidAPI-Key header.
    """
    # You can add RapidAPI key validation here if needed
    # rapidapi_key = request.headers.get("X-RapidAPI-Key")
    # rapidapi_host = request.headers.get("X-RapidAPI-Host")
    
    response = await call_next(request)
    return response


# Include routers
app.include_router(flyers_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint - API info."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "provider": settings.image_provider,
    }


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "detail": "An unexpected error occurred"
        }
    )
