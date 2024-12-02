# OneImage

A powerful command-line tool for image conversion and manipulation.

## Features

- Convert images between different formats
- Resize images with aspect ratio preservation
- Support for multiple image formats (PNG, JPEG, WebP)
- Quality control for lossy formats
- Detailed logging and error reporting
- User-friendly CLI interface with rich formatting

## Installation

```bash
pip install oneimage
```

## Usage

### Convert Images

Convert an image from one format to another:

```bash
oneimage convert input.png output.jpg
```

With quality control:

```bash
oneimage convert input.png output.jpg --quality 85
```

### Resize Images

Resize an image while maintaining aspect ratio:

```bash
# Resize to specific width (height auto-calculated)
oneimage resize input.jpg output.jpg --width 800

# Resize to specific height (width auto-calculated)
oneimage resize input.jpg output.jpg --height 600

# Resize to fit within dimensions (maintains aspect ratio)
oneimage resize input.jpg output.jpg --width 800 --height 600

# Resize to exact dimensions (ignores aspect ratio)
oneimage resize input.jpg output.jpg --width 800 --height 600 --no-aspect-ratio
```

### Additional Options

- `--quality`: Set output quality for JPEG/WebP (1-100)
- `--show-logs`: Display detailed operation logs
- `--log-level`: Set logging detail level (DEBUG/INFO/WARNING/ERROR)

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
