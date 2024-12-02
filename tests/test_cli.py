"""Tests for the CLI interface."""

import pytest
from typer.testing import CliRunner
from pathlib import Path

from oneimage.cli.main import app


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
