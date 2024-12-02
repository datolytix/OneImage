"""Integration tests for OneImage."""

import pytest
from pathlib import Path
from typer.testing import CliRunner
from PIL import Image

from oneimage.cli.main import app
from oneimage.utils.validators import ValidationError
from oneimage.image_converter import ImageConverter


@pytest.fixture
def runner():
    """Provide a CLI runner for testing."""
    return CliRunner()


def test_version(runner):
    """Test version command."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.stdout.lower()


def test_convert_png_to_jpg(runner, test_images, temp_output_dir):
    """Test converting PNG to JPG."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.jpg"
    
    result = runner.invoke(app, [
        "convert",
        str(input_file),
        str(output_file)
    ])
    
    assert result.exit_code == 0
    assert output_file.exists()


def test_convert_with_quality(runner, test_images, temp_output_dir):
    """Test converting with quality parameter."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.jpg"
    
    result = runner.invoke(app, [
        "convert",
        str(input_file),
        str(output_file),
        "--quality", "50"
    ])
    
    assert result.exit_code == 0
    assert output_file.exists()


def test_convert_with_invalid_quality(runner, test_images, temp_output_dir):
    """Test converting with invalid quality value."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.jpg"
    
    result = runner.invoke(app, [
        "convert",
        str(input_file),
        str(output_file),
        "--quality", "101"
    ])
    
    assert result.exit_code == 1
    assert "Error" in result.stdout
    assert not output_file.exists()


def test_convert_nonexistent_file(runner, temp_output_dir):
    """Test converting nonexistent file."""
    result = runner.invoke(app, [
        "convert",
        "nonexistent.png",
        str(temp_output_dir / "output.jpg")
    ])
    
    assert result.exit_code == 1
    assert "Error" in result.stdout


def test_convert_unsupported_format(runner, test_images, temp_output_dir):
    """Test converting to unsupported format."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.xyz"
    
    result = runner.invoke(app, [
        "convert",
        str(input_file),
        str(output_file)
    ])
    
    assert result.exit_code == 1
    assert "Error" in result.stdout
    assert "Unsupported output format 'xyz'" in result.stdout
    assert not output_file.exists()


def test_convert_with_logging(runner, test_images, temp_output_dir, cleanup_logs):
    """Test converting with logging enabled."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.jpg"
    
    result = runner.invoke(app, [
        "--logging",
        "convert",
        str(input_file),
        str(output_file)
    ])
    
    assert result.exit_code == 0
    assert output_file.exists()
    assert Path("logs/oneimage.log").exists()


@pytest.mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR"])
def test_convert_with_log_levels(runner, test_images, temp_output_dir, cleanup_logs, log_level):
    """Test converting with different log levels."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.jpg"
    
    result = runner.invoke(app, [
        "--logging",
        "--log-level", log_level,
        "convert",
        str(input_file),
        str(output_file)
    ])
    
    assert result.exit_code == 0
    assert output_file.exists()
    assert Path("logs/oneimage.log").exists()


def test_resize_image_width_only(temp_output_dir):
    """Test resizing image with only width specified."""
    input_path = Path("tests/data/test_image.png")
    output_path = temp_output_dir / "resized_width.png"
    
    ImageConverter.resize_image(input_path, output_path, width=100)
    
    with Image.open(output_path) as img:
        assert img.size[0] == 100  # width should be exactly 100
        assert img.size[1] > 0     # height should be calculated


def test_resize_image_height_only(temp_output_dir):
    """Test resizing image with only height specified."""
    input_path = Path("tests/data/test_image.png")
    output_path = temp_output_dir / "resized_height.png"
    
    ImageConverter.resize_image(input_path, output_path, height=100)
    
    with Image.open(output_path) as img:
        assert img.size[1] == 100  # height should be exactly 100
        assert img.size[0] > 0     # width should be calculated


def test_resize_image_both_dimensions(temp_output_dir):
    """Test resizing image with both dimensions specified."""
    input_path = Path("tests/data/test_image.png")
    output_path = temp_output_dir / "resized_both.png"
    
    ImageConverter.resize_image(input_path, output_path, width=100, height=100)
    
    with Image.open(output_path) as img:
        # One dimension should be exactly 100, the other might be smaller to maintain aspect ratio
        assert img.size[0] <= 100 and img.size[1] <= 100
        assert img.size[0] == 100 or img.size[1] == 100


def test_resize_image_no_aspect_ratio(temp_output_dir):
    """Test resizing image without maintaining aspect ratio."""
    input_path = Path("tests/data/test_image.png")
    output_path = temp_output_dir / "resized_no_aspect.png"
    
    ImageConverter.resize_image(input_path, output_path, width=100, height=150, maintain_aspect_ratio=False)
    
    with Image.open(output_path) as img:
        assert img.size == (100, 150)  # both dimensions should match exactly


def test_resize_image_invalid_dimensions():
    """Test resizing image with invalid dimensions."""
    input_path = Path("tests/data/test_image.png")
    output_path = Path("output.png")
    
    with pytest.raises(ValidationError, match="At least one of width or height must be specified"):
        ImageConverter.resize_image(input_path, output_path)
    
    with pytest.raises(ValidationError, match="Width must be positive"):
        ImageConverter.resize_image(input_path, output_path, width=-100)
    
    with pytest.raises(ValidationError, match="Height must be positive"):
        ImageConverter.resize_image(input_path, output_path, height=-100)


def test_resize_image_quality(temp_output_dir):
    """Test resizing image with quality parameter."""
    input_path = Path("tests/data/test_image.png")
    output_path = temp_output_dir / "resized_quality.jpg"
    
    ImageConverter.resize_image(input_path, output_path, width=100, quality=50)
    
    # Verify the file was created
    assert output_path.exists()
    
    # Open and verify it's a JPEG
    with Image.open(output_path) as img:
        assert img.format == "JPEG"
        assert img.size[0] == 100


def test_resize_cli_command(runner, temp_output_dir):
    """Test the resize CLI command."""
    input_path = "tests/data/test_image.png"
    output_path = str(temp_output_dir / "resized_cli.png")
    
    # Test basic resize
    result = runner.invoke(app, ["resize", input_path, output_path, "--width", "100"])
    assert result.exit_code == 0
    assert "Successfully resized" in result.stdout
    
    # Test with both dimensions
    result = runner.invoke(app, [
        "resize",
        input_path,
        output_path,
        "--width", "100",
        "--height", "100",
        "--no-aspect-ratio"
    ])
    assert result.exit_code == 0
    assert "Successfully resized" in result.stdout
    
    # Test with invalid input
    result = runner.invoke(app, ["resize", "nonexistent.png", output_path, "--width", "100"])
    assert result.exit_code == 1
    assert "Error" in result.stdout
