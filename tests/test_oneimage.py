"""Integration tests for OneImage."""

import pytest
from pathlib import Path
from typer.testing import CliRunner

from oneimage.cli.main import app
from oneimage.utils.validators import ValidationError


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
