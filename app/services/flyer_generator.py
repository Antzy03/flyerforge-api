"""Core flyer generation service."""

import time
from typing import Optional, List

from ..models.schemas import (
    FlyerRequest,
    FlyerResponse,
    FlyerStyle,
    SIZE_DIMENSIONS,
)
from ..providers.pollinations import PollinationsProvider
from ..config import settings


def get_provider() -> PollinationsProvider:
    """Get the Pollinations image provider."""
    return PollinationsProvider(settings.pollinations_api_key)


# Style-specific prompt modifiers
STYLE_PROMPTS = {
    FlyerStyle.MODERN: "modern minimalist design, clean lines, contemporary typography, sleek professional",
    FlyerStyle.CORPORATE: "professional corporate design, business-like, trustworthy, formal presentation",
    FlyerStyle.PLAYFUL: "fun colorful design, playful elements, friendly approachable style, vibrant",
    FlyerStyle.MINIMAL: "ultra minimal design, lots of white space, simple elegant typography",
    FlyerStyle.BOLD: "bold impactful design, strong typography, eye-catching high contrast",
    FlyerStyle.ELEGANT: "elegant sophisticated design, luxury feel, refined typography, premium",
    FlyerStyle.RETRO: "vintage retro design, nostalgic feel, classic typography, throwback style",
}


class FlyerGeneratorService:
    """Service for generating flyers using AI image providers."""
    
    def __init__(self, provider: Optional[PollinationsProvider] = None):
        """
        Initialize the service.
        
        Args:
            provider: Image provider to use. Defaults based on config.
        """
        self.provider = provider or get_provider()
    
    def _build_prompt(self, request: FlyerRequest) -> str:
        """
        Build an optimized prompt for flyer generation.
        
        Args:
            request: The flyer request with all parameters
            
        Returns:
            A detailed prompt string
        """
        parts = []
        
        # Base flyer instruction
        parts.append("Professional marketing flyer design")
        
        # Business info
        parts.append(f'for "{request.business_name}"')
        
        if request.tagline:
            parts.append(f'with tagline "{request.tagline}"')
        
        # Style
        style_prompt = STYLE_PROMPTS.get(request.style, STYLE_PROMPTS[FlyerStyle.MODERN])
        parts.append(f"in {style_prompt} style")
        
        # Color
        if request.primary_color:
            parts.append(f"featuring {request.primary_color} as the primary color")
        
        # Description
        if request.description:
            parts.append(f"showcasing: {request.description}")
        
        # Elements
        if request.include_elements:
            elements = ", ".join(request.include_elements)
            parts.append(f"including visual elements: {elements}")
        
        # Additional text
        if request.additional_text:
            parts.append(f'displaying text: "{request.additional_text}"')
        
        # Quality modifiers
        parts.append("high quality print-ready design, professional typography, visually appealing layout")
        
        return ", ".join(parts)
    
    async def generate(self, request: FlyerRequest) -> FlyerResponse:
        """
        Generate a flyer based on the request.
        
        Args:
            request: The flyer generation request
            
        Returns:
            FlyerResponse with the generated image URL
        """
        start_time = time.time()
        
        try:
            # Build the prompt
            prompt = self._build_prompt(request)
            
            # Get dimensions for the requested size
            width, height = SIZE_DIMENSIONS[request.size]
            
            # Generate the image
            image_url = await self.provider.generate(
                prompt=prompt,
                width=width,
                height=height,
            )
            
            generation_time = int((time.time() - start_time) * 1000)
            
            return FlyerResponse(
                success=True,
                image_url=image_url,
                prompt_used=prompt,
                provider=self.provider.name,
                generation_time_ms=generation_time,
            )
            
        except Exception as e:
            return FlyerResponse(
                success=False,
                provider=self.provider.name,
                error=str(e),
            )
