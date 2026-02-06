"""Pydantic models for request/response schemas."""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class FlyerStyle(str, Enum):
    """Available flyer design styles."""
    MODERN = "modern"
    CORPORATE = "corporate"
    PLAYFUL = "playful"
    MINIMAL = "minimal"
    BOLD = "bold"
    ELEGANT = "elegant"
    RETRO = "retro"


class FlyerSize(str, Enum):
    """Available flyer sizes/formats."""
    SOCIAL_SQUARE = "social_square"      # 1080x1080 - Instagram
    SOCIAL_PORTRAIT = "social_portrait"  # 1080x1350 - Instagram
    SOCIAL_STORY = "social_story"        # 1080x1920 - Stories
    A4_PORTRAIT = "a4_portrait"          # A4 vertical
    A4_LANDSCAPE = "a4_landscape"        # A4 horizontal
    POSTER = "poster"                    # Large poster format


# Size dimensions mapping
SIZE_DIMENSIONS = {
    FlyerSize.SOCIAL_SQUARE: (1024, 1024),
    FlyerSize.SOCIAL_PORTRAIT: (1024, 1280),
    FlyerSize.SOCIAL_STORY: (768, 1365),
    FlyerSize.A4_PORTRAIT: (768, 1024),
    FlyerSize.A4_LANDSCAPE: (1024, 768),
    FlyerSize.POSTER: (1024, 1536),
}


class FlyerRequest(BaseModel):
    """Request model for flyer generation."""
    
    business_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the business",
        examples=["Coffee Corner"]
    )
    
    tagline: Optional[str] = Field(
        None,
        max_length=150,
        description="Business tagline or slogan",
        examples=["Fresh brews, cozy vibes"]
    )
    
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Brief description of the business or offer",
        examples=["Local coffee shop featuring artisan pastries and specialty drinks"]
    )
    
    style: FlyerStyle = Field(
        FlyerStyle.MODERN,
        description="Visual style for the flyer"
    )
    
    primary_color: Optional[str] = Field(
        None,
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Primary brand color in hex format",
        examples=["#8B4513"]
    )
    
    size: FlyerSize = Field(
        FlyerSize.SOCIAL_SQUARE,
        description="Output size/format"
    )
    
    include_elements: Optional[List[str]] = Field(
        None,
        max_length=5,
        description="Specific elements to include in the design",
        examples=[["coffee cup", "pastries", "cozy interior"]]
    )
    
    additional_text: Optional[str] = Field(
        None,
        max_length=200,
        description="Additional text to include (e.g., offers, contact info)",
        examples=["20% OFF this weekend! Visit us at 123 Main St"]
    )


class FlyerResponse(BaseModel):
    """Response model for flyer generation."""
    
    success: bool = Field(
        ...,
        description="Whether generation was successful"
    )
    
    image_url: Optional[str] = Field(
        None,
        description="URL to the generated image"
    )
    
    prompt_used: Optional[str] = Field(
        None,
        description="The prompt used for generation (for debugging)"
    )
    
    provider: str = Field(
        ...,
        description="Image provider used"
    )
    
    generation_time_ms: Optional[int] = Field(
        None,
        description="Time taken to generate in milliseconds"
    )
    
    error: Optional[str] = Field(
        None,
        description="Error message if generation failed"
    )


class StyleInfo(BaseModel):
    """Information about an available style."""
    name: str
    value: str
    description: str


class SizeInfo(BaseModel):
    """Information about an available size."""
    name: str
    value: str
    dimensions: str
    use_case: str
