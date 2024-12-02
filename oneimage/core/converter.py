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

    @staticmethod
    def resize_image(
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect_ratio: bool = True,
        quality: Optional[Union[int, str]] = None,
    ) -> None:
        """
        Resize an image to specified dimensions.

        Parameters
        ----------
        input_path : Union[str, Path]
            Path to input image file
        output_path : Union[str, Path]
            Path where resized image will be saved
        width : Optional[int]
            Target width in pixels
        height : Optional[int]
            Target height in pixels
        maintain_aspect_ratio : bool
            If True, maintains aspect ratio when resizing
        quality : Optional[Union[int, str]]
            Quality setting for lossy formats (1-100)

        Raises
        ------
        ValidationError
            If any validation fails
        """
        try:
            logger.info(f"Starting resize: {input_path} -> {output_path}")

            # Validate paths
            input_path = validate_image_path(input_path, should_exist=True)
            output_path = validate_image_path(output_path, should_exist=False)

            # Validate quality
            quality_value = validate_quality(quality) or DEFAULT_QUALITY

            # Validate dimensions
            if not width and not height:
                raise ValidationError("At least one of width or height must be specified")
            if width and width <= 0:
                raise ValidationError(f"Width must be positive, got {width}")
            if height and height <= 0:
                raise ValidationError(f"Height must be positive, got {height}")

            logger.debug(f"Resizing with params: width={width}, height={height}, maintain_aspect_ratio={maintain_aspect_ratio}")

            # Open and resize image
            with Image.open(input_path) as img:
                original_width, original_height = img.size
                logger.debug(f"Original size: {original_width}x{original_height}")

                # Calculate new dimensions
                if maintain_aspect_ratio:
                    if not width:
                        # Calculate width based on height
                        aspect_ratio = original_width / original_height
                        width = int(height * aspect_ratio)
                    elif not height:
                        # Calculate height based on width
                        aspect_ratio = original_height / original_width
                        height = int(width * aspect_ratio)
                    else:
                        # Both dimensions specified, maintain aspect ratio using the most constraining dimension
                        width_ratio = width / original_width
                        height_ratio = height / original_height
                        if width_ratio < height_ratio:
                            height = int(original_height * width_ratio)
                        else:
                            width = int(original_width * height_ratio)
                else:
                    # Use original dimension if not specified
                    width = width or original_width
                    height = height or original_height

                logger.debug(f"New size: {width}x{height}")

                # Convert RGBA to RGB if saving as JPEG
                if output_path.suffix.lower() in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
                    logger.debug("Converting RGBA to RGB for JPEG output")
                    img = img.convert('RGB')

                # Perform resize
                resized_img = img.resize((width, height), Image.Resampling.LANCZOS)

                # Prepare save parameters
                save_params = {}
                if output_path.suffix.lower() in ['.jpg', '.jpeg', '.webp']:
                    save_params['quality'] = quality_value

                # Save resized image
                resized_img.save(output_path, **save_params)

            logger.info(f"Successfully resized image to {width}x{height}")

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            raise ValidationError(f"Error during image resize: {str(e)}")


logger.debug("Converter module loaded")
