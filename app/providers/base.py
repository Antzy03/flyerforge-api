"""Abstract base class for image generation providers."""

from abc import ABC, abstractmethod
from typing import Tuple


class ImageProvider(ABC):
    """Base interface for image generation providers."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""
        pass
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        width: int,
        height: int,
    ) -> str:
        """
        Generate an image from a prompt.
        
        Args:
            prompt: The text prompt for generation
            width: Image width in pixels
            height: Image height in pixels
            
        Returns:
            URL to the generated image
            
        Raises:
            Exception: If generation fails
        """
        pass
