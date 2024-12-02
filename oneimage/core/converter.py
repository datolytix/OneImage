"""Core image conversion functionality."""

from pathlib import Path
from typing import Optional, Union

from PIL import Image
from loguru import logger

from ..config.settings import DEFAULT_QUALITY
from ..utils.validators import (
    ValidationError,
    validate_image_path,
    validate_quality,
)


class ImageConverter:
    """Class for handling image conversion operations."""

    @staticmethod
    def convert_image(
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        quality: Optional[Union[int, str]] = None,
    ) -> None:
        """
        Convert an image from one format to another.

        Parameters
        ----------
        input_path : Union[str, Path]
            Path to input image file
        output_path : Union[str, Path]
            Path where converted image will be saved
        quality : Optional[Union[int, str]], optional
            Quality setting for lossy formats (1-100), by default None

        Raises
        ------
        ValidationError
            If any validation fails
        """
        try:
            # Log operation start
            logger.info(f"Starting conversion: {input_path} -> {output_path}")
            
            # Validate input path
            input_path = validate_image_path(input_path, should_exist=True)
            logger.debug(f"Input path validated: {input_path}")
            
            # Validate output path
            output_path = validate_image_path(output_path, should_exist=False)
            logger.debug(f"Output path validated: {output_path}")
            
            # Validate quality
            quality_value = validate_quality(quality) or DEFAULT_QUALITY
            logger.debug(f"Quality validated: {quality_value}")

            # Open and convert image
            logger.debug("Opening input image")
            with Image.open(input_path) as img:
                # Get original format and mode
                original_format = img.format
                original_mode = img.mode
                logger.debug(f"Image opened: format={original_format}, mode={original_mode}")

                # Convert RGBA to RGB if saving as JPEG
                out_ext = output_path.suffix.lower()
                if out_ext in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
                    logger.debug("Converting RGBA to RGB for JPEG output")
                    img = img.convert('RGB')
                
                # Prepare save parameters
                save_params = {}
                
                # Add quality parameter for supported formats
                if out_ext in ['.jpg', '.jpeg', '.webp']:
                    save_params['quality'] = quality_value
                    logger.debug(f"Using quality: {quality_value}")
                
                # Save with appropriate parameters
                logger.debug(f"Saving image with parameters: {save_params}")
                img.save(output_path, **save_params)

            logger.info(f"Successfully converted {input_path} to {output_path}")

        except ValidationError:
            # Re-raise validation errors as they are already properly formatted
            raise
        except Exception as e:
            logger.error(f"Error converting {input_path} to {output_path}: {str(e)}")
            raise ValidationError(f"Error during image conversion: {str(e)}")


logger.debug("Converter module loaded")
