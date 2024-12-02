# OneImage

A powerful command-line tool for image conversion and manipulation.

## Features

- Convert images between different formats (PNG, JPEG, WebP)
- Resize images with aspect ratio preservation
- Rotate images with customizable angles
- High-quality image processing
- Comprehensive error handling
- User-friendly command-line interface

## Installation

```bash
pip install oneimage
```

## Usage

### Commands

#### Convert
Convert images between different formats:
```bash
oneimage convert input.png output.jpg
oneimage convert input.webp output.jpg --quality 95
```

#### Resize
Resize images with various options:
```bash
oneimage resize input.jpg output.jpg --width 800
oneimage resize input.png output.png --height 600 --keep-aspect
```

#### Rotate
Rotate images by any angle:
```bash
# Basic 90-degree rotation
oneimage rotate input.jpg output.jpg

# Custom angle with quality setting
oneimage rotate input.png output.jpg --angle 45 --quality 95

# Rotate without expanding canvas
oneimage rotate input.webp output.webp --angle 180 --expand false
```

### Options

#### Global Options
- `--log-level`: Set logging level (DEBUG, INFO, WARNING, ERROR)

#### Format-specific Options
- `--quality`: Set quality for lossy formats (1-100, default: 85)

#### Resize Options
- `--width`: Target width in pixels
- `--height`: Target height in pixels
- `--keep-aspect`: Maintain aspect ratio (default: true)

#### Rotate Options
- `--angle`: Rotation angle in degrees (default: 90)
- `--expand`: Expand canvas to fit rotated image (default: true)

## Supported Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- WebP (.webp)
- Additional formats supported by Pillow

## Development

### Requirements

- Python 3.8+
- Poetry (recommended) or pip

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/oneimage.git
cd oneimage
```

2. Install dependencies:
```bash
poetry install
# or
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details
