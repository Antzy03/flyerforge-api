"""Flyer generation API endpoints."""

from fastapi import APIRouter, HTTPException
from typing import List

from ..models.schemas import (
    FlyerRequest,
    FlyerResponse,
    FlyerStyle,
    FlyerSize,
    StyleInfo,
    SizeInfo,
    SIZE_DIMENSIONS,
)
from ..services.flyer_generator import FlyerGeneratorService


router = APIRouter(prefix="/flyers", tags=["Flyers"])

# Initialize the service
flyer_service = FlyerGeneratorService()


@router.post(
    "/generate",
    response_model=FlyerResponse,
    summary="Generate a flyer",
    description="Generate a professional flyer or poster using AI based on your business information and style preferences.",
)
async def generate_flyer(request: FlyerRequest) -> FlyerResponse:
    """
    Generate a marketing flyer using AI.
    
    - **business_name**: Your business name (required)
    - **tagline**: Catchy tagline or slogan
    - **description**: Brief description of what you're promoting
    - **style**: Visual style (modern, corporate, playful, etc.)
    - **primary_color**: Brand color in hex format (#RRGGBB)
    - **size**: Output size (social_square, a4_portrait, poster, etc.)
    - **include_elements**: Visual elements to include
    - **additional_text**: Extra text like offers or contact info
    """
    result = await flyer_service.generate(request)
    
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)
    
    return result


@router.get(
    "/styles",
    response_model=List[StyleInfo],
    summary="List available styles",
    description="Get a list of all available flyer design styles.",
)
async def list_styles() -> List[StyleInfo]:
    """Get all available flyer styles."""
    styles = [
        StyleInfo(name="Modern", value="modern", description="Clean, minimalist contemporary design"),
        StyleInfo(name="Corporate", value="corporate", description="Professional business-focused design"),
        StyleInfo(name="Playful", value="playful", description="Fun, colorful, and approachable"),
        StyleInfo(name="Minimal", value="minimal", description="Ultra-simple with lots of white space"),
        StyleInfo(name="Bold", value="bold", description="High contrast, impactful design"),
        StyleInfo(name="Elegant", value="elegant", description="Sophisticated, luxury feel"),
        StyleInfo(name="Retro", value="retro", description="Vintage, nostalgic aesthetic"),
    ]
    return styles


@router.get(
    "/sizes",
    response_model=List[SizeInfo],
    summary="List available sizes",
    description="Get a list of all available flyer sizes and formats.",
)
async def list_sizes() -> List[SizeInfo]:
    """Get all available flyer sizes."""
    sizes = [
        SizeInfo(
            name="Social Square",
            value="social_square",
            dimensions="1024x1024",
            use_case="Instagram posts, Facebook"
        ),
        SizeInfo(
            name="Social Portrait",
            value="social_portrait",
            dimensions="1024x1280",
            use_case="Instagram portrait posts"
        ),
        SizeInfo(
            name="Social Story",
            value="social_story",
            dimensions="768x1365",
            use_case="Instagram/Facebook Stories"
        ),
        SizeInfo(
            name="A4 Portrait",
            value="a4_portrait",
            dimensions="768x1024",
            use_case="Printable flyers, handouts"
        ),
        SizeInfo(
            name="A4 Landscape",
            value="a4_landscape",
            dimensions="1024x768",
            use_case="Horizontal flyers, banners"
        ),
        SizeInfo(
            name="Poster",
            value="poster",
            dimensions="1024x1536",
            use_case="Large format printing"
        ),
    ]
    return sizes
