"""Watermark module for OneImage."""
from pathlib import Path
from typing import Optional, Union, Tuple
import os

from PIL import Image, ImageDraw, ImageFont, ImageColor
from loguru import logger

from oneimage.utils.validators import validate_image_path, validate_quality, ValidationError
from oneimage.core.base import DEFAULT_QUALITY

class WatermarkProcessor:
    """Handles image watermarking operations."""

    FONT_PATHS = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",  # macOS
        "C:\\Windows\\Fonts\\arial.ttf",  # Windows
    ]

    @staticmethod
    def _get_font(size: int) -> ImageFont.FreeTypeFont:
        """Get a font with the specified size."""
        # Try system fonts first
        for font_path in WatermarkProcessor.FONT_PATHS:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except OSError:
                    continue

        # If no system fonts work, use default font
        try:
            # For newer Pillow versions that support size with load_default
            return ImageFont.load_default(size=size)
        except TypeError:
            # For older Pillow versions, create a larger default font
            default_font = ImageFont.load_default()
            # Create a new image with the default font and scale it
            img = Image.new('L', (size * 2, size * 2))
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), "A", font=default_font, fill=255)
            img = img.resize((size * 3, size * 3), Image.Resampling.LANCZOS)
            return ImageFont.load_default()

    @staticmethod
    def add_watermark(
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        text: str,
        position: str = "bottom-right",
        opacity: int = 50,
        font_size: int = 36,
        font_color: str = "white",
        quality: Optional[Union[int, str]] = None,
    ) -> None:
        """
        Add a text watermark to an image.

        Parameters
        ----------
        input_path : Union[str, Path]
            Path to input image file
        output_path : Union[str, Path]
            Path where watermarked image will be saved
        text : str
            Text to use as watermark
        position : str
            Position of watermark (top-left, top-right, bottom-left, bottom-right, center)
        opacity : int
            Opacity of watermark (0-100)
        font_size : int
            Font size for watermark text
        font_color : str
            Color of watermark text
        quality : Optional[Union[int, str]]
            Quality setting for lossy formats (1-100)

        Raises
        ------
        ValidationError
            If any validation fails
        """
        try:
            logger.info(f"Adding watermark to: {input_path}")
            
            # Validate paths
            input_path = validate_image_path(input_path, should_exist=True)
            output_path = validate_image_path(output_path, should_exist=False)
            
            # Validate quality
            quality_value = validate_quality(quality)
            
            # Validate opacity
            if not 0 <= opacity <= 100:
                raise ValidationError(f"Opacity must be between 0 and 100, got {opacity}")
            
            # Validate font size
            if font_size <= 0:
                raise ValidationError(f"Font size must be greater than 0, got {font_size}")

            # Open image
            with Image.open(input_path) as img:
                # Create a copy to work with
                watermarked = img.copy()
                
                # Create transparent layer for watermark
                watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(watermark)
                
                # Get font with specified size
                font = WatermarkProcessor._get_font(font_size)
                logger.debug(f"Using font: {font}")
                
                # Get text size
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                # Calculate position
                x, y = WatermarkProcessor._calculate_position(
                    position, watermark.size, (text_width, text_height)
                )
                
                # Convert color string to RGB tuple
                try:
                    rgb_color = ImageColor.getrgb(font_color)
                except ValueError:
                    logger.warning(f"Invalid color '{font_color}', using white")
                    rgb_color = ImageColor.getrgb("white")
                
                # Draw watermark text
                draw.text(
                    (x, y),
                    text,
                    font=font,
                    fill=(*rgb_color, int(255 * opacity / 100))
                )
                
                # Composite watermark onto image
                watermarked = Image.alpha_composite(
                    watermarked.convert('RGBA'),
                    watermark
                )
                
                # Convert RGBA to RGB if saving as JPEG
                if output_path.suffix.lower() in ['.jpg', '.jpeg']:
                    if watermarked.mode == 'RGBA':
                        watermarked = watermarked.convert('RGB')
                
                # Prepare save parameters
                save_params = {}
                if output_path.suffix.lower() in ['.jpg', '.jpeg', '.webp']:
                    save_params['quality'] = quality_value or DEFAULT_QUALITY
                
                # Save watermarked image
                watermarked.save(output_path, **save_params)
            
            logger.info("Successfully added watermark")
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error adding watermark: {str(e)}")
            raise ValidationError(f"Error during watermarking: {str(e)}")
    
    @staticmethod
    def _calculate_position(
        position: str,
        image_size: Tuple[int, int],
        text_size: Tuple[int, int],
        padding: int = 20
    ) -> Tuple[int, int]:
        """Calculate watermark position."""
        img_width, img_height = image_size
        text_width, text_height = text_size
        
        positions = {
            "top-left": (padding, padding),
            "top-right": (img_width - text_width - padding, padding),
            "bottom-left": (padding, img_height - text_height - padding),
            "bottom-right": (img_width - text_width - padding, img_height - text_height - padding),
            "center": ((img_width - text_width) // 2, (img_height - text_height) // 2),
        }
        
        if position not in positions:
            logger.warning(f"Invalid position '{position}', using bottom-right")
            position = "bottom-right"
        
        return positions[position]
