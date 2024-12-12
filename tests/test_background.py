"""Tests for background removal functionality."""

import pytest
from PIL import Image
from pathlib import Path

from oneimage.core.background import BackgroundRemover
from oneimage.utils.validators import ValidationError


def test_background_remover_init():
    """Test BackgroundRemover initialization."""
    remover = BackgroundRemover()
    assert remover._sessions == {}


def test_get_session():
    """Test session management."""
    remover = BackgroundRemover()
    
    # Get session for default model
    session1 = remover._get_session("u2net")
    assert "u2net" in remover._sessions
    
    # Get same session again
    session2 = remover._get_session("u2net")
    assert session1 == session2


def test_remove_background_invalid_path(tmp_path):
    """Test background removal with invalid input path."""
    remover = BackgroundRemover()
    invalid_path = tmp_path / "nonexistent.jpg"
    
    with pytest.raises(ValidationError):
        remover.remove_background(invalid_path)


def test_remove_background_invalid_alpha_matting_params(test_images):
    """Test background removal with invalid alpha matting parameters."""
    remover = BackgroundRemover()
    input_path = test_images["rgb.png"]
    
    # Test invalid foreground threshold
    with pytest.raises(ValidationError):
        remover.remove_background(
            input_path,
            alpha_matting=True,
            alpha_matting_foreground_threshold=300
        )
    
    # Test invalid background threshold
    with pytest.raises(ValidationError):
        remover.remove_background(
            input_path,
            alpha_matting=True,
            alpha_matting_background_threshold=-10
        )
    
    # Test invalid erode size
    with pytest.raises(ValidationError):
        remover.remove_background(
            input_path,
            alpha_matting=True,
            alpha_matting_erode_size=-5
        )


def test_remove_background_basic(test_images, mocker):
    """Test basic background removal functionality."""
    # Mock rembg.remove to avoid actual model loading and processing
    mock_output = Image.new("RGBA", (100, 100), (255, 0, 0, 0))
    mock_remove = mocker.patch("oneimage.core.background.remove", return_value=mock_output)
    
    remover = BackgroundRemover()
    input_path = test_images["rgb.png"]
    
    # Test basic background removal
    result = remover.remove_background(input_path)
    
    # Verify the mock was called correctly
    mock_remove.assert_called_once()
    assert isinstance(result, Image.Image)
    assert result.mode == "RGBA"  # Background removal should produce RGBA image


def test_remove_background_with_alpha_matting(test_images, mocker):
    """Test background removal with alpha matting enabled."""
    # Mock rembg.remove
    mock_output = Image.new("RGBA", (100, 100), (255, 0, 0, 0))
    mock_remove = mocker.patch("oneimage.core.background.remove", return_value=mock_output)
    
    remover = BackgroundRemover()
    input_path = test_images["rgb.png"]
    
    # Test with alpha matting
    result = remover.remove_background(
        input_path,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10
    )
    
    # Verify the mock was called with correct parameters
    mock_remove.assert_called_once()
    call_kwargs = mock_remove.call_args.kwargs
    assert call_kwargs["alpha_matting"] is True
    assert call_kwargs["alpha_matting_foreground_threshold"] == 240
    assert call_kwargs["alpha_matting_background_threshold"] == 10
    assert call_kwargs["alpha_matting_erode_size"] == 10


def test_remove_background_different_models(test_images, mocker):
    """Test background removal with different models."""
    # Mock rembg functions
    mock_output = Image.new("RGBA", (100, 100), (255, 0, 0, 0))
    mocker.patch("oneimage.core.background.remove", return_value=mock_output)
    mock_session = mocker.patch("oneimage.core.background.new_session")
    
    remover = BackgroundRemover()
    input_path = test_images["rgb.png"]
    
    # Test with different models
    models = ["u2net", "u2netp", "u2net_human_seg"]
    for model in models:
        result = remover.remove_background(input_path, model_name=model)
        assert isinstance(result, Image.Image)
        assert model in remover._sessions
