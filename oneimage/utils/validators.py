"""Validation utilities for OneImage."""

import os
import stat
from pathlib import Path
from typing import Optional, Union

from loguru import logger

from ..config.settings import SUPPORTED_FORMATS


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_quality(quality: Optional[Union[int, str]]) -> Optional[int]:
    """
    Validate quality parameter for image conversion.

    Parameters
    ----------
    quality : Optional[Union[int, str]]
        Quality value to validate. Can be None, int, or str that can be converted to int.

    Returns
    -------
    Optional[int]
        Validated quality value.

    Raises
    ------
    ValidationError
        If quality value is invalid.
    """
    if quality is None:
        return None

    # First check if it's a boolean or float
    if isinstance(quality, (bool, float)):
        raise ValidationError(f"Quality must be an integer between 1 and 100, got {quality}")

    try:
        quality_int = int(quality)
    except (ValueError, TypeError):
        raise ValidationError(f"Quality must be an integer between 1 and 100, got {quality}")

    if not 1 <= quality_int <= 100:
        raise ValidationError(f"Quality must be between 1 and 100, got {quality_int}")

    return quality_int


def validate_image_path(path: Union[str, Path], should_exist: bool = True) -> Path:
    """
    Validate image file path.

    Parameters
    ----------
    path : Union[str, Path]
        Path to validate.
    should_exist : bool, optional
        Whether the file should exist, by default True.

    Returns
    -------
    Path
        Validated path.

    Raises
    ------
    ValidationError
        If path is invalid.
    """
    try:
        # Convert to Path and resolve
        path = Path(path).resolve()
        logger.debug(f"Validating path: {path} (should_exist={should_exist})")

        if should_exist:
            # Check existence
            if not path.exists():
                raise ValidationError(f"File does not exist: {path}")
            
            # Check if it's a file
            if not path.is_file():
                raise ValidationError(f"Path is not a file: {path}")
            
            # Check file permissions
            try:
                mode = path.stat().st_mode
                if not mode & stat.S_IRUSR:
                    raise ValidationError(f"File is not readable: {path}")
            except OSError as e:
                raise ValidationError(f"Cannot access file permissions: {path} ({str(e)})")
            
            # Check file size (optional)
            try:
                size = path.stat().st_size
                logger.debug(f"File size: {size / 1024:.1f}KB")
            except OSError as e:
                logger.warning(f"Could not check file size: {path} ({str(e)})")
            
            # Check if input format is supported
            suffix = path.suffix.lower()
            if suffix not in SUPPORTED_FORMATS:
                supported_formats_str = ', '.join(sorted(SUPPORTED_FORMATS))
                raise ValidationError(
                    f"Unsupported input format '{suffix[1:]}'. Supported formats: {supported_formats_str}"
                )
        else:
            # Check if parent directory exists and is writable
            parent = path.parent
            if not parent.exists():
                try:
                    parent.mkdir(parents=True, exist_ok=True)
                    logger.debug(f"Created parent directory: {parent}")
                except Exception as e:
                    raise ValidationError(f"Cannot create output directory: {str(e)}")
            
            # Check write permissions
            try:
                if not os.access(parent, os.W_OK):
                    raise ValidationError(f"Output directory is not writable: {parent}")
            except OSError as e:
                raise ValidationError(f"Cannot check directory permissions: {parent} ({str(e)})")
            
            # Check if output format is supported
            suffix = path.suffix.lower()
            if suffix not in SUPPORTED_FORMATS:
                supported_formats_str = ', '.join(sorted(SUPPORTED_FORMATS))
                raise ValidationError(
                    f"Unsupported output format '{suffix[1:]}'. Supported formats: {supported_formats_str}"
                )

        return path

    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid path: {str(e)}")


logger.debug("Validators module loaded")
