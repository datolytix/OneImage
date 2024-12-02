"""Test configuration and fixtures for OneImage."""

import os
import shutil
from pathlib import Path

import pytest
from PIL import Image

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "test_data"
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output"


@pytest.fixture(scope="session", autouse=True)
def setup_test_dirs():
    """Create and cleanup test directories."""
    # Create test directories
    TEST_DATA_DIR.mkdir(exist_ok=True)
    TEST_OUTPUT_DIR.mkdir(exist_ok=True)

    yield

    # Cleanup after all tests
    shutil.rmtree(TEST_OUTPUT_DIR)


@pytest.fixture(scope="session")
def test_images():
    """Create test images in various formats."""
    # Create a simple test image
    img_size = (100, 100)
    test_files = {
        "rgb.png": ("RGB", (255, 0, 0)),  # Red image
        "rgba.png": ("RGBA", (0, 255, 0, 255)),  # Green image with alpha
        "grayscale.png": ("L", 128),  # Gray image
        "test.jpg": ("RGB", (0, 0, 255)),  # Blue image
        "test.webp": ("RGB", (255, 255, 0)),  # Yellow image
    }

    created_files = {}
    for filename, (mode, color) in test_files.items():
        filepath = TEST_DATA_DIR / filename
        if not filepath.exists():
            img = Image.new(mode, img_size, color)
            img.save(filepath)
        created_files[filename] = filepath

    return created_files


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary directory for test outputs."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def cleanup_logs():
    """Clean up log files after tests."""
    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    yield
    
    # Clean up log files
    if log_dir.exists():
        shutil.rmtree(log_dir)


@pytest.fixture
def mock_image(mocker):
    """Mock PIL Image for testing."""
    mock_img = mocker.MagicMock()
    mock_img.save = mocker.MagicMock()
    mock_img.convert = mocker.MagicMock(return_value=mock_img)
    
    mock_open = mocker.patch("PIL.Image.open", return_value=mock_img)
    return mock_img, mock_open
