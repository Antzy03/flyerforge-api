"""Pollinations.ai image provider with API key authentication."""

import httpx
import urllib.parse
import base64
from .base import ImageProvider


class PollinationsProvider(ImageProvider):
    """
    Image generation using Pollinations.ai API.
    
    Uses gen.pollinations.ai endpoint with Bearer token auth.
    """
    
    API_URL = "https://gen.pollinations.ai/image"
    
    def __init__(self, api_key: str = None):
        """
        Initialize the provider.
        
        Args:
            api_key: Pollinations API key (sk_ or pk_ prefix)
        """
        self.api_key = api_key
    
    @property
    def name(self) -> str:
        return "pollinations"
    
    async def generate(
        self,
        prompt: str,
        width: int,
        height: int,
    ) -> str:
        """
        Generate image using Pollinations API.
        
        The API returns the image directly, so we make the request
        and return a data URL or the direct API URL.
        
        Args:
            prompt: Text prompt for the image
            width: Image width
            height: Image height
            
        Returns:
            URL to the generated image
        """
        # URL encode the prompt for the path
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Build the full URL with query params
        url = (
            f"{self.API_URL}/{encoded_prompt}"
            f"?width={width}&height={height}&model=gptimage&nologo=true"
        )
        
        # Set up headers with Bearer auth
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        # Make the request and get the image
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.get(url, headers=headers, follow_redirects=True)
            response.raise_for_status()
            
            # Get the image bytes
            image_bytes = response.content
            content_type = response.headers.get("content-type", "image/jpeg")
            
            # Convert to data URL for easy display
            b64_image = base64.b64encode(image_bytes).decode("utf-8")
            data_url = f"data:{content_type};base64,{b64_image}"
            
            return data_url
