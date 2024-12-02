"""Configuration settings for OneImage."""

from typing import Final, Set

# Supported image formats (lowercase)
SUPPORTED_FORMATS: Final[Set[str]] = {
    '.jpg', '.jpeg', '.png', '.webp'
}

# Maximum file size (100MB)
MAX_IMAGE_SIZE: Final[int] = 100 * 1024 * 1024

# Quality settings
MIN_QUALITY: Final[int] = 1
MAX_QUALITY: Final[int] = 100

# Default quality for lossy formats
DEFAULT_QUALITY: Final[int] = 85

# Logging settings
DEFAULT_LOG_FORMAT: Final[str] = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
DEFAULT_LOG_LEVEL: Final[str] = "INFO"
DEFAULT_LOG_ROTATION: Final[str] = "1 MB"
