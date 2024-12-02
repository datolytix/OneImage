"""Tests for the image converter functionality."""

import pytest
from pathlib import Path
from PIL import Image

from oneimage.core.converter import ImageConverter
from oneimage.utils.validators import ValidationError


def test_convert_png_to_jpg(test_images, temp_output_dir):
    """Test converting PNG to JPG."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.jpg"
    
    ImageConverter.convert_image(input_file, output_file)
    
    assert output_file.exists()
    with Image.open(output_file) as img:
        assert img.format == "JPEG"
        assert img.mode == "RGB"


def test_convert_jpg_to_webp(test_images, temp_output_dir):
    """Test converting JPG to WebP."""
    input_file = test_images["test.jpg"]
    output_file = temp_output_dir / "output.webp"
    
    ImageConverter.convert_image(input_file, output_file)
    
    assert output_file.exists()
    with Image.open(output_file) as img:
        assert img.format == "WEBP"


def test_convert_with_quality(test_images, temp_output_dir):
    """Test converting with quality parameter."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.jpg"
    
    ImageConverter.convert_image(input_file, output_file, quality=50)
    
    assert output_file.exists()
    # Check file size is smaller than with default quality
    default_output = temp_output_dir / "default.jpg"
    ImageConverter.convert_image(input_file, default_output)
    
    assert output_file.stat().st_size < default_output.stat().st_size


def test_convert_rgba_to_jpg(test_images, temp_output_dir):
    """Test converting RGBA image to JPG (which doesn't support alpha)."""
    input_file = test_images["rgba.png"]
    output_file = temp_output_dir / "output.jpg"
    
    ImageConverter.convert_image(input_file, output_file)
    
    assert output_file.exists()
    with Image.open(output_file) as img:
        assert img.mode == "RGB"  # Should be converted to RGB


def test_convert_grayscale(test_images, temp_output_dir):
    """Test converting grayscale image."""
    input_file = test_images["grayscale.png"]
    output_file = temp_output_dir / "output.png"
    
    ImageConverter.convert_image(input_file, output_file)
    
    assert output_file.exists()
    with Image.open(output_file) as img:
        assert img.mode == "L"  # Should preserve grayscale mode


def test_convert_invalid_input_path():
    """Test converting with invalid input path."""
    with pytest.raises(ValidationError):
        ImageConverter.convert_image(
            Path("nonexistent.png"),
            Path("output.jpg")
        )


def test_convert_invalid_output_format(test_images, temp_output_dir):
    """Test converting to unsupported format."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.invalid"
    
    with pytest.raises(ValidationError):
        ImageConverter.convert_image(input_file, output_file)


def test_convert_with_invalid_quality(test_images, temp_output_dir):
    """Test converting with invalid quality value."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.jpg"
    
    with pytest.raises(ValidationError):
        ImageConverter.convert_image(input_file, output_file, quality=101)


@pytest.mark.parametrize("quality", [-1, 0, 101, 1000])
def test_convert_with_out_of_range_quality(test_images, temp_output_dir, quality):
    """Test converting with out of range quality values."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.jpg"
    
    with pytest.raises(ValidationError):
        ImageConverter.convert_image(input_file, output_file, quality=quality)
