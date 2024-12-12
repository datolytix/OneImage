"""Background removal functionality for OneImage."""

from pathlib import Path
from typing import Optional, Union
import os

from PIL import Image
from rembg import remove, new_session
from loguru import logger

from oneimage.utils.validators import validate_image_path, ValidationError


class BackgroundRemover:
    """Handles background removal operations using rembg."""

    def __init__(self):
        """Initialize the BackgroundRemover."""
        self._sessions = {}

    def _get_session(self, model_name: str):
        """Get or create a session for the specified model."""
        if model_name not in self._sessions:
            self._sessions[model_name] = new_session(model_name)
        return self._sessions[model_name]

    def remove_background(
        self,
        input_path: Union[str, Path],
        model_name: str = "u2net",
        alpha_matting: bool = False,
        alpha_matting_foreground_threshold: int = 240,
        alpha_matting_background_threshold: int = 10,
        alpha_matting_erode_size: int = 10,
    ) -> Image.Image:
        """
        Remove the background from an image.

        Parameters
        ----------
        input_path : Union[str, Path]
            Path to input image file
        model_name : str, optional
            Name of the model to use (u2net, u2netp, u2net_human_seg)
        alpha_matting : bool, optional
            Whether to use alpha matting for better edge detection
        alpha_matting_foreground_threshold : int, optional
            Alpha matting foreground threshold (0-255)
        alpha_matting_background_threshold : int, optional
            Alpha matting background threshold (0-255)
        alpha_matting_erode_size : int, optional
            Alpha matting erode size

        Returns
        -------
        PIL.Image.Image
            Image with background removed

        Raises
        ------
        ValidationError
            If any validation fails
        """
        try:
            # Validate input path
            input_path = validate_image_path(input_path, should_exist=True)

            # Validate alpha matting parameters
            if alpha_matting:
                if not 0 <= alpha_matting_foreground_threshold <= 255:
                    raise ValidationError(
                        f"Alpha matting foreground threshold must be between 0 and 255, got {alpha_matting_foreground_threshold}"
                    )
                if not 0 <= alpha_matting_background_threshold <= 255:
                    raise ValidationError(
                        f"Alpha matting background threshold must be between 0 and 255, got {alpha_matting_background_threshold}"
                    )
                if alpha_matting_erode_size < 0:
                    raise ValidationError(
                        f"Alpha matting erode size must be non-negative, got {alpha_matting_erode_size}"
                    )

            # Load the image
            input_image = Image.open(input_path)

            # Get the session for the specified model
            session = self._get_session(model_name)

            # Remove the background
            output_image = remove(
                input_image,
                session=session,
                alpha_matting=alpha_matting,
                alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                alpha_matting_background_threshold=alpha_matting_background_threshold,
                alpha_matting_erode_size=alpha_matting_erode_size,
            )

            return output_image

        except Exception as e:
            logger.error(f"Error removing background: {str(e)}")
            raise
