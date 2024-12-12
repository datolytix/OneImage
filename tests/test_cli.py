"""Tests for CLI functionality."""
import pytest
from pathlib import Path
from typer.testing import CliRunner
from PIL import Image
from unittest.mock import Mock

from oneimage.cli.main import app

# Test constants
TEST_WIDTH = 100
TEST_HEIGHT = 100

def create_test_image(path: Path, mode: str = 'RGB'):
    """Create a test image for CLI tests."""
    img = Image.new(mode, (TEST_WIDTH, TEST_HEIGHT), color='white')
    img.save(path)


@pytest.fixture
def runner():
    """Provide a CLI runner for testing."""
    return CliRunner()


def test_version(runner):
    """Test --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.stdout.lower()


def test_help(runner):
    """Test --help flag."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout
    assert "Options" in result.stdout


def test_convert_command_help(runner):
    """Test convert command help."""
    result = runner.invoke(app, ["convert", "--help"])
    assert result.exit_code == 0
    assert "Convert an image" in result.stdout


def test_convert_basic(runner, test_images, temp_output_dir):
    """Test basic conversion command."""
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
    """Test conversion with quality parameter."""
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


def test_convert_with_logging(runner, test_images, temp_output_dir, cleanup_logs):
    """Test conversion with logging enabled."""
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


def test_convert_nonexistent_file(runner, temp_output_dir):
    """Test conversion with nonexistent input file."""
    result = runner.invoke(app, [
        "convert",
        "nonexistent.png",
        str(temp_output_dir / "output.jpg")
    ])
    
    assert result.exit_code != 0
    assert "Error" in result.stdout


def test_convert_invalid_format(runner, test_images, temp_output_dir):
    """Test conversion with invalid output format."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.invalid"
    
    result = runner.invoke(app, [
        "convert",
        str(input_file),
        str(output_file)
    ])
    
    assert result.exit_code != 0
    assert "Error" in result.stdout


def test_convert_invalid_quality(runner, test_images, temp_output_dir):
    """Test conversion with invalid quality value."""
    input_file = test_images["rgb.png"]
    output_file = temp_output_dir / "output.jpg"
    
    result = runner.invoke(app, [
        "convert",
        str(input_file),
        str(output_file),
        "--quality", "101"
    ])
    
    assert result.exit_code != 0
    assert "Error" in result.stdout


@pytest.mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR"])
def test_log_levels(runner, test_images, temp_output_dir, cleanup_logs, log_level):
    """Test different log levels."""
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


def test_watermark_command_help(runner):
    """Test watermark command help output."""
    result = runner.invoke(app, ["watermark", "--help"])
    assert result.exit_code == 0
    assert "Add a text watermark" in result.stdout


def test_watermark_basic(runner, tmp_path):
    """Test basic watermark command."""
    input_path = tmp_path / "test_input.png"
    output_path = tmp_path / "test_output.png"
    create_test_image(input_path)
    
    result = runner.invoke(app, [
        "watermark",
        str(input_path),
        str(output_path),
        "--text", "Test Watermark"
    ])
    
    assert result.exit_code == 0
    assert output_path.exists()


def test_watermark_with_options(runner, tmp_path):
    """Test watermark command with all options."""
    input_path = tmp_path / "test_input.png"
    output_path = tmp_path / "test_output.jpg"
    create_test_image(input_path)
    
    result = runner.invoke(app, [
        "watermark",
        str(input_path),
        str(output_path),
        "--text", "Test",
        "--position", "center",
        "--opacity", "75",
        "--font-size", "24",
        "--font-color", "red",
        "--quality", "90"
    ])
    
    assert result.exit_code == 0
    assert output_path.exists()


def test_watermark_invalid_input(runner, tmp_path):
    """Test watermark command with invalid input path."""
    input_path = tmp_path / "nonexistent.png"
    output_path = tmp_path / "test_output.png"
    
    result = runner.invoke(app, [
        "watermark",
        str(input_path),
        str(output_path),
        "--text", "Test"
    ])
    
    assert result.exit_code == 1
    assert not output_path.exists()


def test_watermark_invalid_opacity(runner, tmp_path):
    """Test watermark command with invalid opacity."""
    input_path = tmp_path / "test_input.png"
    output_path = tmp_path / "test_output.png"
    create_test_image(input_path)
    
    result = runner.invoke(app, [
        "watermark",
        str(input_path),
        str(output_path),
        "--text", "Test",
        "--opacity", "101"
    ])
    
    assert result.exit_code == 1
    assert not output_path.exists()


def test_remove_bg_command(runner, test_images, temp_output_dir, mocker):
    """Test the remove-bg command."""
    # Mock background removal to avoid actual processing
    mock_output = Image.new("RGBA", (100, 100), (255, 0, 0, 0))
    mocker.patch("oneimage.core.background.remove", return_value=mock_output)
    
    input_path = test_images["rgb.png"]
    output_path = temp_output_dir / "output_nobg.png"
    
    # Test basic command
    result = runner.invoke(app, ["remove-bg", str(input_path), str(output_path)])
    assert result.exit_code == 0
    assert "Successfully removed background" in result.stdout
    assert output_path.exists()


def test_remove_bg_command_with_options(runner, test_images, temp_output_dir, mocker):
    """Test the remove-bg command with various options."""
    # Mock background removal
    mock_output = Image.new("RGBA", (100, 100), (255, 0, 0, 0))
    mock_remove = mocker.patch("oneimage.core.background.remove", return_value=mock_output)
    
    input_path = test_images["rgb.png"]
    output_path = temp_output_dir / "output_nobg_options.png"
    
    # Test with all options
    result = runner.invoke(app, [
        "remove-bg",
        str(input_path),
        str(output_path),
        "--model", "u2net_human_seg",
        "--alpha-matting",
        "--alpha-matting-foreground-threshold", "230",
        "--alpha-matting-background-threshold", "20",
        "--alpha-matting-erode-size", "15",
        "--quality", "90"
    ])
    
    assert result.exit_code == 0
    assert "Successfully removed background" in result.stdout
    assert output_path.exists()
    
    # Verify the mock was called with correct parameters
    mock_remove.assert_called_once()
    call_kwargs = mock_remove.call_args.kwargs
    assert call_kwargs["alpha_matting"] is True
    assert call_kwargs["alpha_matting_foreground_threshold"] == 230
    assert call_kwargs["alpha_matting_background_threshold"] == 20
    assert call_kwargs["alpha_matting_erode_size"] == 15


def test_remove_bg_command_invalid_input(runner, temp_output_dir):
    """Test the remove-bg command with invalid input."""
    # Test with non-existent input file
    result = runner.invoke(app, [
        "remove-bg",
        "nonexistent.jpg",
        str(temp_output_dir / "output.png")
    ])
    assert result.exit_code == 1
    assert "Error" in result.stdout


def test_remove_bg_command_invalid_params(runner, test_images, temp_output_dir):
    """Test the remove-bg command with invalid parameters."""
    input_path = test_images["rgb.png"]
    output_path = temp_output_dir / "output_invalid.png"
    
    # Test with invalid alpha matting parameters
    result = runner.invoke(app, [
        "remove-bg",
        str(input_path),
        str(output_path),
        "--alpha-matting",
        "--alpha-matting-foreground-threshold", "300"  # Invalid value
    ])
    assert result.exit_code == 1
    assert "Error" in result.stdout
