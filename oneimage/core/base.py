"""Base converter module for OneImage."""
from pathlib import Path
from typing import Optional, Union

from PIL import Image
from loguru import logger

from oneimage.utils.validators import validate_image_path, validate_quality

DEFAULT_QUALITY = 85

class BaseConverter:
    """Base class for image operations."""

    @staticmethod
    def _prepare_save_params(output_path: Path, quality: Optional[int] = None) -> dict:
        """
        Prepare save parameters for image output.

        Parameters
        ----------
        output_path : Path
            Path where image will be saved
        quality : Optional[int]
            Quality setting for lossy formats (1-100)

        Returns
        -------
        dict
            Dictionary of save parameters
        """
        save_params = {}
        if output_path.suffix.lower() in ['.jpg', '.jpeg', '.webp']:
            save_params['quality'] = quality or DEFAULT_QUALITY
        return save_params

    @staticmethod
    def _handle_rgba_to_rgb(img: Image.Image, output_path: Path) -> Image.Image:
        """
        Convert RGBA to RGB if saving as JPEG.

        Parameters
        ----------
        img : Image.Image
            Input image
        output_path : Path
            Output path to determine format

        Returns
        -------
        Image.Image
            Converted image if needed, otherwise original image
        """
        if output_path.suffix.lower() in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
            logger.debug("Converting RGBA to RGB for JPEG output")
            return img.convert('RGB')
        return img
