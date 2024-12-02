"""Test suite for OneImage."""

import pytest
from pathlib import Path
from typer.testing import CliRunner
from PIL import Image

from oneimage.cli.main import app
from oneimage.utils.validators import ValidationError
from oneimage.core.converter import ImageConverter

TEST_WIDTH = 100
TEST_HEIGHT = 100

@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary directory for test outputs."""
    return tmp_path


def create_test_image(path: Path, size=(100, 100), color='red'):
    """Create a test image for testing."""
    img = Image.new('RGB', size, color)
    img.save(path)
    return path


def test_resize_image_width_only(temp_output_dir):
    """Test resizing image with only width specified."""
    input_path = create_test_image(temp_output_dir / "original.png")
    output_path = temp_output_dir / "resized_width.png"
    
    ImageConverter.resize_image(input_path, output_path, width=50)
    
    with Image.open(output_path) as img:
        assert img.size[0] == 50  # width should be exactly 50
        assert img.size[1] > 0     # height should be calculated


def test_resize_image_height_only(temp_output_dir):
    """Test resizing image with only height specified."""
    input_path = create_test_image(temp_output_dir / "original.png")
    output_path = temp_output_dir / "resized_height.png"
    
    ImageConverter.resize_image(input_path, output_path, height=50)
    
    with Image.open(output_path) as img:
        assert img.size[1] == 50  # height should be exactly 50
        assert img.size[0] > 0     # width should be calculated


def test_resize_image_both_dimensions(temp_output_dir):
    """Test resizing image with both dimensions specified."""
    input_path = create_test_image(temp_output_dir / "original.png", size=(200, 100))
    output_path = temp_output_dir / "resized_both.png"
    
    ImageConverter.resize_image(input_path, output_path, width=100, height=100)
    
    with Image.open(output_path) as img:
        # One dimension should be exactly 100, the other might be smaller to maintain aspect ratio
        assert img.size[0] <= 100 and img.size[1] <= 100
        assert img.size[0] == 100 or img.size[1] == 50  # maintain aspect ratio


def test_resize_image_no_aspect_ratio(temp_output_dir):
    """Test resizing image without maintaining aspect ratio."""
    input_path = create_test_image(temp_output_dir / "original.png")
    output_path = temp_output_dir / "resized_no_aspect.png"
    
    ImageConverter.resize_image(input_path, output_path, width=50, height=75, maintain_aspect_ratio=False)
    
    with Image.open(output_path) as img:
        assert img.size == (50, 75)  # both dimensions should match exactly


def test_resize_image_invalid_dimensions(temp_output_dir):
    """Test resizing image with invalid dimensions."""
    input_path = create_test_image(temp_output_dir / "original.png")
    output_path = temp_output_dir / "invalid.png"
    
    with pytest.raises(ValidationError, match="At least one of width or height must be specified"):
        ImageConverter.resize_image(input_path, output_path)
    
    with pytest.raises(ValidationError, match="Width must be positive"):
        ImageConverter.resize_image(input_path, output_path, width=-100)
    
    with pytest.raises(ValidationError, match="Height must be positive"):
        ImageConverter.resize_image(input_path, output_path, height=-100)


def test_resize_image_quality(temp_output_dir):
    """Test resizing image with quality parameter."""
    input_path = create_test_image(temp_output_dir / "original.png")
    output_path = temp_output_dir / "resized_quality.jpg"
    
    ImageConverter.resize_image(input_path, output_path, width=50, quality=50)
    
    # Verify the file was created
    assert output_path.exists()
    
    # Open and verify it's a JPEG
    with Image.open(output_path) as img:
        assert img.format == "JPEG"
        assert img.size[0] == 50


def test_resize_cli_command(runner, temp_output_dir):
    """Test the resize CLI command."""
    input_path = create_test_image(temp_output_dir / "original.png")
    output_path = temp_output_dir / "resized_cli.png"
    
    # Test basic resize
    result = runner.invoke(app, ["resize", str(input_path), str(output_path), "--width", "50"])
    assert result.exit_code == 0
    assert "Successfully resized" in result.stdout
    
    # Test with both dimensions
    result = runner.invoke(app, [
        "resize",
        str(input_path),
        str(output_path),
        "--width", "50",
        "--height", "50",
        "--no-aspect-ratio"
    ])
    assert result.exit_code == 0
    assert "Successfully resized" in result.stdout
    
    # Test with invalid input
    result = runner.invoke(app, ["resize", "nonexistent.png", str(output_path), "--width", "50"])
    assert result.exit_code == 1
    assert "Error" in result.stdout


def test_convert_image(temp_output_dir):
    """Test basic image conversion."""
    input_path = create_test_image(temp_output_dir / "original.png")
    output_path = temp_output_dir / "converted.jpg"
    
    ImageConverter.convert_image(input_path, output_path)
    assert output_path.exists()


def test_convert_cli_command(runner, temp_output_dir):
    """Test the convert CLI command."""
    input_path = create_test_image(temp_output_dir / "original.png")
    output_path = temp_output_dir / "converted.jpg"
    
    result = runner.invoke(app, ["convert", str(input_path), str(output_path)])
    assert result.exit_code == 0
    assert output_path.exists()


def test_rotate_image_90_degrees(tmp_path):
    """Test rotating an image by 90 degrees."""
    # Create test image
    input_path = tmp_path / "test_input.png"
    output_path = tmp_path / "test_output.png"
    create_test_image(input_path)

    # Rotate image
    converter = ImageConverter()
    converter.rotate_image(input_path, output_path, angle=90)

    # Verify output exists and is valid
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.size[0] == TEST_HEIGHT  # Width and height should be swapped
        assert img.size[1] == TEST_WIDTH


def test_rotate_image_custom_angle(tmp_path):
    """Test rotating an image by a custom angle."""
    input_path = tmp_path / "test_input.png"
    output_path = tmp_path / "test_output.png"
    create_test_image(input_path)

    converter = ImageConverter()
    converter.rotate_image(input_path, output_path, angle=45, expand=True)

    assert output_path.exists()
    with Image.open(output_path) as img:
        # For 45 degrees with expand=True, dimensions should be larger
        assert img.size[0] > TEST_WIDTH
        assert img.size[1] > TEST_HEIGHT


def test_rotate_image_no_expand(tmp_path):
    """Test rotating an image without expanding."""
    input_path = tmp_path / "test_input.png"
    output_path = tmp_path / "test_output.png"
    create_test_image(input_path)

    converter = ImageConverter()
    converter.rotate_image(input_path, output_path, angle=45, expand=False)

    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.size[0] == TEST_WIDTH  # Dimensions should remain the same
        assert img.size[1] == TEST_HEIGHT


def test_rotate_image_with_quality(tmp_path):
    """Test rotating an image with quality setting."""
    input_path = tmp_path / "test_input.png"
    output_path = tmp_path / "test_output.jpg"
    create_test_image(input_path)

    converter = ImageConverter()
    converter.rotate_image(input_path, output_path, angle=90, quality=50)

    assert output_path.exists()
    # Verify it's a JPEG
    with Image.open(output_path) as img:
        assert img.format == "JPEG"


def test_rotate_cli_command(tmp_path):
    """Test the rotate CLI command."""
    input_path = tmp_path / "test_input.png"
    output_path = tmp_path / "test_output.png"
    create_test_image(input_path)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["rotate", str(input_path), str(output_path), "--angle", "90"]
    )

    assert result.exit_code == 0
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.size[0] == TEST_HEIGHT
        assert img.size[1] == TEST_WIDTH
