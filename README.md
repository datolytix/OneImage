# OneImage

A powerful and user-friendly command-line tool for image manipulation.

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
# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install the package
pip install -e .
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

## Best Practices

1. **Quality Settings**
   - Use higher quality (90-100) for important images
   - Use moderate quality (75-85) for web images
   - Use lower quality (60-75) for thumbnails

2. **Format Selection**
   - PNG: Best for screenshots, graphics with text
   - JPEG: Ideal for photographs
   - WebP: Good balance for web use

3. **Performance**
   - Process large batches of images in smaller chunks
   - Monitor system resources during bulk operations
   - Use appropriate quality settings to manage file sizes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest -v`
5. Submit a pull request

## License

MIT License - See LICENSE file for details
