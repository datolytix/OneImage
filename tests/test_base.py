"""Tests for base converter functionality."""
import pytest
from pathlib import Path
from PIL import Image

from oneimage.core.base import BaseConverter, DEFAULT_QUALITY

def test_prepare_save_params_jpg():
    """Test prepare save params for JPEG format."""
    output_path = Path("test.jpg")
    params = BaseConverter._prepare_save_params(output_path)
    assert params["quality"] == DEFAULT_QUALITY

def test_prepare_save_params_jpeg():
    """Test prepare save params for JPEG format (alternate extension)."""
    output_path = Path("test.jpeg")
    params = BaseConverter._prepare_save_params(output_path)
    assert params["quality"] == DEFAULT_QUALITY

def test_prepare_save_params_webp():
    """Test prepare save params for WebP format."""
    output_path = Path("test.webp")
    params = BaseConverter._prepare_save_params(output_path)
    assert params["quality"] == DEFAULT_QUALITY

def test_prepare_save_params_png():
    """Test prepare save params for PNG format."""
    output_path = Path("test.png")
    params = BaseConverter._prepare_save_params(output_path)
    assert params == {}

def test_prepare_save_params_custom_quality():
    """Test prepare save params with custom quality."""
    output_path = Path("test.jpg")
    quality = 95
    params = BaseConverter._prepare_save_params(output_path, quality)
    assert params["quality"] == quality

def test_handle_rgba_to_rgb_jpg():
    """Test RGBA to RGB conversion for JPEG."""
    img = Image.new('RGBA', (100, 100))
    output_path = Path("test.jpg")
    
    converted = BaseConverter._handle_rgba_to_rgb(img, output_path)
    assert converted.mode == "RGB"

def test_handle_rgba_to_rgb_png():
    """Test RGBA to RGB conversion for PNG (should not convert)."""
    img = Image.new('RGBA', (100, 100))
    output_path = Path("test.png")
    
    converted = BaseConverter._handle_rgba_to_rgb(img, output_path)
    assert converted.mode == "RGBA"

def test_handle_rgba_to_rgb_rgb_input():
    """Test RGBA to RGB conversion with RGB input (should not convert)."""
    img = Image.new('RGB', (100, 100))
    output_path = Path("test.jpg")
    
    converted = BaseConverter._handle_rgba_to_rgb(img, output_path)
    assert converted.mode == "RGB"

def test_handle_rgba_to_rgb_case_insensitive():
    """Test RGBA to RGB conversion with uppercase extension."""
    img = Image.new('RGBA', (100, 100))
    output_path = Path("test.JPG")
    
    converted = BaseConverter._handle_rgba_to_rgb(img, output_path)
    assert converted.mode == "RGB"
