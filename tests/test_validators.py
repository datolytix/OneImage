"""Tests for validation utilities."""

import os
import pytest
from pathlib import Path

from oneimage.utils.validators import (
    ValidationError,
    validate_quality,
    validate_image_path,
)
from oneimage.config.settings import SUPPORTED_FORMATS


@pytest.mark.parametrize("quality", [
    1, 50, 100,  # Valid integers
    "1", "50", "100",  # Valid strings
    None,  # None is valid (uses default)
])
def test_validate_quality_valid(quality):
    """Test validate_quality with valid inputs."""
    result = validate_quality(quality)
    if quality is not None:
        assert isinstance(result, int)
        assert 1 <= result <= 100


@pytest.mark.parametrize("quality", [
    0, 101,  # Out of range integers
    "0", "101",  # Out of range strings
    "abc", "",  # Invalid strings
    3.14, [], {},  # Invalid types
])
def test_validate_quality_invalid(quality):
    """Test validate_quality with invalid inputs."""
    with pytest.raises(ValidationError):
        validate_quality(quality)


def test_validate_image_path_existing(tmp_path):
    """Test validate_image_path with existing file."""
    # Create a test PNG file
    test_file = tmp_path / "test.png"
    test_file.write_bytes(b"dummy image content")
    
    # Should not raise for existing file
    result = validate_image_path(test_file, should_exist=True)
    assert isinstance(result, Path)
    assert result.exists()


def test_validate_image_path_nonexistent(tmp_path):
    """Test validate_image_path with nonexistent file."""
    test_file = tmp_path / "nonexistent.png"
    
    # Should raise for nonexistent file when should_exist=True
    with pytest.raises(ValidationError, match="does not exist"):
        validate_image_path(test_file, should_exist=True)
    
    # Should not raise for nonexistent file when should_exist=False
    result = validate_image_path(test_file, should_exist=False)
    assert isinstance(result, Path)
    assert not result.exists()


def test_validate_image_path_unsupported_format(tmp_path):
    """Test validate_image_path with unsupported format."""
    test_file = tmp_path / "test.xyz"
    
    with pytest.raises(ValidationError, match="Unsupported"):
        validate_image_path(test_file, should_exist=False)


def test_validate_image_path_directory(tmp_path):
    """Test validate_image_path with directory."""
    with pytest.raises(ValidationError, match="not a file"):
        validate_image_path(tmp_path, should_exist=True)


def test_validate_image_path_no_permissions(tmp_path):
    """Test validate_image_path with permission issues."""
    # Create a test file without read permissions
    test_file = tmp_path / "test.png"
    test_file.write_bytes(b"dummy image content")
    os.chmod(test_file, 0o000)
    
    try:
        with pytest.raises(ValidationError, match="not readable"):
            validate_image_path(test_file, should_exist=True)
    finally:
        # Restore permissions to allow cleanup
        os.chmod(test_file, 0o666)


def test_validate_image_path_create_parent_dirs(tmp_path):
    """Test validate_image_path creating parent directories."""
    deep_path = tmp_path / "a" / "b" / "c" / "test.png"
    
    result = validate_image_path(deep_path, should_exist=False)
    assert isinstance(result, Path)
    assert deep_path.parent.exists()


def test_validate_image_path_supported_formats():
    """Test validate_image_path with all supported formats."""
    for fmt in SUPPORTED_FORMATS:
        path = Path(f"test{fmt}")
        # Should not raise for supported formats
        validate_image_path(path, should_exist=False)
