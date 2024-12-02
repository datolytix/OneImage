"""Tests for watermark functionality."""
import pytest
from pathlib import Path
from PIL import Image, ImageFont

from oneimage.core.watermark import WatermarkProcessor
from oneimage.utils.validators import ValidationError

# Test constants
TEST_WIDTH = 100
TEST_HEIGHT = 100

class MockFont:
    """Mock font for testing."""
    def getbbox(self, text, *args, **kwargs):
        """Return bounding box for text."""
        return (0, 0, 50, 20)  # Fixed size for testing (left, top, right, bottom)
    
    def getmask(self, text, *args, **kwargs):
        """Create a simple mask for text."""
        mask = Image.new('L', (50, 20), 255)
        return mask.im  # Return the core image object

@pytest.fixture
def mock_font(monkeypatch):
    """Mock font for testing."""
    def mock_truetype(*args, **kwargs):
        return MockFont()
    monkeypatch.setattr(ImageFont, "truetype", mock_truetype)
    monkeypatch.setattr(ImageFont, "load_default", lambda: MockFont())

def create_test_image(path: Path, mode: str = 'RGB'):
    """Create a test image for watermark tests."""
    img = Image.new(mode, (TEST_WIDTH, TEST_HEIGHT), color='white')
    img.save(path)

@pytest.fixture
def test_image(tmp_path):
    """Create a test image."""
    input_path = tmp_path / "test_input.png"
    create_test_image(input_path)
    return input_path

def test_add_watermark_basic(tmp_path, test_image, mock_font):
    """Test basic watermark addition."""
    output_path = tmp_path / "test_output.png"
    
    WatermarkProcessor.add_watermark(
        test_image,
        output_path,
        text="Test Watermark"
    )
    
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.size == (TEST_WIDTH, TEST_HEIGHT)

def test_add_watermark_with_options(tmp_path, test_image, mock_font):
    """Test watermark with custom options."""
    output_path = tmp_path / "test_output.jpg"
    
    WatermarkProcessor.add_watermark(
        test_image,
        output_path,
        text="Custom Test",
        position="center",
        opacity=75,
        font_size=24,
        font_color="red",
        quality=90
    )
    
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.format == "JPEG"

def test_add_watermark_rgba_to_jpg(tmp_path, mock_font):
    """Test watermark with RGBA to JPEG conversion."""
    input_path = tmp_path / "test_input.png"
    output_path = tmp_path / "test_output.jpg"
    create_test_image(input_path, mode='RGBA')
    
    WatermarkProcessor.add_watermark(
        input_path,
        output_path,
        text="RGBA Test"
    )
    
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.mode == "RGB"

def test_add_watermark_invalid_position(tmp_path, test_image, mock_font):
    """Test watermark with invalid position."""
    output_path = tmp_path / "test_output.png"
    
    WatermarkProcessor.add_watermark(
        test_image,
        output_path,
        text="Test",
        position="invalid"  # Should default to bottom-right
    )
    
    assert output_path.exists()

def test_add_watermark_invalid_opacity(tmp_path, test_image, mock_font):
    """Test watermark with invalid opacity."""
    output_path = tmp_path / "test_output.png"
    
    with pytest.raises(ValidationError):
        WatermarkProcessor.add_watermark(
            test_image,
            output_path,
            text="Test",
            opacity=101
        )

def test_add_watermark_all_positions(tmp_path, test_image, mock_font):
    """Test watermark in all valid positions."""
    positions = ["top-left", "top-right", "bottom-left", "bottom-right", "center"]
    
    for pos in positions:
        output_path = tmp_path / f"test_output_{pos}.png"
        
        WatermarkProcessor.add_watermark(
            test_image,
            output_path,
            text=f"Test {pos}",
            position=pos
        )
        
        assert output_path.exists()

def test_add_watermark_invalid_color(tmp_path, test_image, mock_font):
    """Test watermark with invalid color."""
    output_path = tmp_path / "test_output.png"
    
    WatermarkProcessor.add_watermark(
        test_image,
        output_path,
        text="Test",
        font_color="invalid_color"  # Should default to white
    )
    
    assert output_path.exists()
