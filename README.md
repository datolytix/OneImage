# OneImage

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/datolytix/OneImage/workflows/CI/badge.svg)](https://github.com/datolytix/OneImage/actions)
[![Coverage Status](https://codecov.io/gh/datolytix/OneImage/branch/main/graph/badge.svg)](https://codecov.io/gh/datolytix/OneImage)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-red.svg)]()

> ⚠️ **Note**: This project is currently in alpha version. APIs and features may change without notice.

A powerful and user-friendly command-line tool for image manipulation, built with Python. OneImage provides a comprehensive suite of image processing capabilities, making it easy to perform common image operations like format conversion, resizing, rotation, and watermarking through a simple command-line interface. Whether you're a developer automating image processing tasks or a user looking for a straightforward tool to manage your images, OneImage offers the flexibility and features you need.

## Features

- Format Conversion: Convert between PNG, JPEG, and WebP formats
- Image Resizing: Scale images with precise control over dimensions
- Image Rotation: Rotate images with customizable angles
- Text Watermarks: Add customizable text watermarks to images
- Quality Control: Fine-tune compression for lossy formats
- Aspect Ratio: Maintain or adjust image proportions
- Error Handling: Comprehensive validation and error reporting
- Logging: Detailed operation logging with configurable levels

## Installation

```bash
# Clone the repository
git clone https://github.com/datolytix/OneImage.git
cd OneImage

# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install development dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .

# Run tests to verify installation
pytest -v

# Run linting
pylint oneimage tests

# Generate coverage report
pytest --cov=oneimage tests/
coverage html  # Generate HTML coverage report
```

## Development Setup

1. **Dependencies**
   - Python 3.8 or higher
   - Pillow library for image processing
   - Click for CLI interface
   - pytest for testing
   - pylint for code quality

2. **Project Structure**
   ```
   oneimage/
   ├── oneimage/           # Main package directory
   │   ├── core/           # Core functionality
   │   ├── utils/          # Utility functions
   │   └── config/         # Configuration
   ├── tests/              # Test files
   ├── docs/               # Documentation
   ├── requirements.txt    # Project dependencies
   └── setup.py           # Package setup file
   ```

3. **Environment Variables**
   ```bash
   # Optional: Set custom configuration
   export ONEIMAGE_LOG_LEVEL=DEBUG
   export ONEIMAGE_DEFAULT_QUALITY=90
   ```

## Quick Start

```bash
# Convert image format
oneimage convert input.png output.jpg

# Resize image
oneimage resize input.jpg output.jpg --width 800

# Rotate image
oneimage rotate input.png output.png --angle 90

# Add watermark
oneimage watermark input.jpg output.jpg --text "Copyright 2024"
```

## Detailed Usage

### Format Conversion

Convert images between supported formats with optional quality settings:

```bash
# Basic conversion
oneimage convert input.png output.jpg

# Set quality for lossy formats (1-100)
oneimage convert input.png output.jpg --quality 95

# With detailed logging
oneimage convert input.png output.webp --log-level DEBUG
```

### Image Resizing

Resize images with various options:

```bash
# Resize by width (maintains aspect ratio)
oneimage resize input.jpg output.jpg --width 800

# Resize by height (maintains aspect ratio)
oneimage resize input.jpg output.jpg --height 600

# Resize with exact dimensions
oneimage resize input.jpg output.jpg --width 800 --height 600 --no-aspect-ratio

# Resize with quality control
oneimage resize input.png output.jpg --width 1024 --quality 90
```

### Image Rotation

Rotate images with customizable settings:

```bash
# 90-degree rotation (default)
oneimage rotate input.jpg output.jpg

# Custom angle
oneimage rotate input.png output.png --angle 45

# Rotate without expanding canvas
oneimage rotate input.jpg output.jpg --angle 30 --expand false

# Rotate with quality control
oneimage rotate input.png output.jpg --angle 180 --quality 95
```

### Image Watermarking

Add text watermarks to images with various customization options:

```bash
# Basic watermark
oneimage watermark input.jpg output.jpg --text "Copyright 2024"

# Customized watermark
oneimage watermark input.png output.png \
    --text "My Watermark" \
    --position center \
    --opacity 75 \
    --font-size 48 \
    --font-color "red"

# Watermark with quality control
oneimage watermark input.png output.jpg \
    --text "Confidential" \
    --position top-right \
    --quality 95
```

## Advanced Usage

### Batch Processing

Process multiple images at once using shell commands:

```bash
# Convert all JPGs in current directory to WebP
for file in *.jpg; do
    oneimage convert "$file" "${file%.jpg}.webp"
done

# Resize all PNGs to width 800px
for file in *.png; do
    oneimage resize "$file" "resized_${file}" --width 800
done
```

### Pipeline Operations

Combine multiple operations:

```bash
# Resize, rotate, and add watermark in one pipeline
oneimage resize input.jpg temp1.jpg --width 800 && \
oneimage rotate temp1.jpg temp2.jpg --angle 45 && \
oneimage watermark temp2.jpg output.jpg --text "Copyright" && \
rm temp1.jpg temp2.jpg
```

### Debug Mode

Run with detailed logging for troubleshooting:

```bash
# Enable debug logging
oneimage --log-level DEBUG convert input.png output.jpg

# Save logs to file
oneimage --log-level DEBUG --log-file process.log convert input.png output.jpg
```

## Command Options

### Global Options

- `--log-level`: Set logging level
  - Values: DEBUG, INFO, WARNING, ERROR
  - Default: INFO
  - Example: `--log-level DEBUG`

### Format-specific Options

- `--quality`: Quality setting for lossy formats (JPEG, WebP)
  - Range: 1-100
  - Default: 85
  - Example: `--quality 95`

### Resize Options

- `--width`: Target width in pixels
  - Example: `--width 800`

- `--height`: Target height in pixels
  - Example: `--height 600`

- `--keep-aspect`: Maintain aspect ratio
  - Default: true
  - Example: `--no-aspect-ratio`

### Rotate Options

- `--angle`: Rotation angle in degrees
  - Default: 90
  - Example: `--angle 45`

- `--expand`: Expand canvas to fit rotated image
  - Default: true
  - Example: `--expand false`

### Watermark Options

- `--text`: Watermark text content
  - Required
  - Example: `--text "Copyright 2024"`

- `--position`: Watermark position
  - Values: top-left, top-right, bottom-left, bottom-right, center
  - Default: bottom-right
  - Example: `--position center`

- `--opacity`: Watermark opacity
  - Range: 0-100
  - Default: 50
  - Example: `--opacity 75`

- `--font-size`: Text size in pixels
  - Default: 36
  - Example: `--font-size 48`

- `--font-color`: Text color
  - Default: white
  - Example: `--font-color "red"`

## Supported Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- WebP (.webp)

## Error Handling

The tool provides detailed error messages for common issues:

- Invalid input/output paths
- Unsupported file formats
- Invalid quality settings
- Permission errors
- File size limits
- Memory constraints

## Logging

Control logging verbosity with `--log-level`:

```bash
# Detailed debug information
oneimage convert input.png output.jpg --log-level DEBUG

# Only warnings and errors
oneimage convert input.png output.jpg --log-level WARNING
```

## Performance Tips

1. **Memory Management**
   - Process large images in batches
   - Monitor system memory usage
   - Use appropriate quality settings

2. **Storage Optimization**
   - Choose appropriate formats:
     * PNG for graphics/screenshots
     * JPEG for photos (quality 80-90)
     * WebP for web content

3. **Batch Processing**
   - Use shell scripts for bulk operations
   - Process files in parallel when possible
   - Monitor CPU usage

## Troubleshooting

Common issues and solutions:

1. **Installation Issues**
   ```bash
   # Upgrade pip
   pip install --upgrade pip

   # Clear pip cache
   pip cache purge

   # Install with verbose output
   pip install -e . -v
   ```

2. **Permission Errors**
   ```bash
   # Check file permissions
   ls -l input.jpg

   # Change file permissions if needed
   chmod 644 input.jpg
   ```

3. **Memory Errors**
   - Reduce image dimensions before processing
   - Free up system memory
   - Process fewer images simultaneously

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest -v`
5. Submit a pull request

## License

MIT License - See LICENSE file for details
