# OneImage

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-alpha-orange)

A powerful command-line tool for image format conversion and manipulation, built with Python.

## Features

- 🖼️ Convert images between popular formats (PNG, JPG, WebP)
- 🎨 Quality control for lossy formats
- 📊 Progress tracking with rich terminal output
- 📝 Comprehensive logging system
- ⚡ Shell completion support
- 🛡️ Type-safe implementation
- 🐛 Robust error handling

## Installation

### From PyPI (Recommended)

```bash
pip install oneimage
```

### From Source

```bash
git clone https://github.com/JuanS3/oneimage.git
cd oneimage
pip install -e .
```

## Quick Start

Convert an image with a single command:

```bash
oneimage convert input.jpg output.webp
```

## Usage Guide

### Basic Commands

1. **Simple Conversion**
   ```bash
   oneimage convert input.jpg output.webp
   ```

2. **Convert with Quality Control**
   ```bash
   oneimage convert input.png output.jpg --quality 90
   ```

3. **Enable Detailed Logging**
   ```bash
   oneimage --logging convert input.png output.webp
   ```

4. **Set Specific Log Level**
   ```bash
   oneimage --logging --log-level DEBUG convert input.png output.webp
   ```

5. **View Version Information**
   ```bash
   oneimage --version
   ```

### Command-line Options

#### Global Options

These options apply to all commands:

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--logging` | `-l` | Enable detailed logging output | `False` |
| `--log-level` | - | Set logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `--version` | `-v` | Show version information | - |
| `--help` | `-h` | Show help message | - |

#### Convert Command Options

Options specific to the `convert` command:

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--quality` | `-q` | Set output quality (1-100) for lossy formats | Format dependent |

### Supported Formats

Currently supported image formats:

- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- WebP (`.webp`)

### Shell Completion

OneImage supports shell completion for all commands and options. To enable it:

```bash
# For bash
oneimage --install-completion bash

# For zsh
oneimage --install-completion zsh

# For fish
oneimage --install-completion fish
```

### Logging System

OneImage provides a comprehensive logging system:

- Log files are stored in `logs/oneimage.log`
- Logs rotate automatically when they reach 1MB
- Console logging is optional (enable with `--logging`)
- Four log levels available: DEBUG, INFO, WARNING, ERROR

## Examples

### Basic Image Conversion

Convert a PNG to JPEG:
```bash
oneimage convert image.png output.jpg
```

### Quality-Controlled Conversion

Convert with 85% quality:
```bash
oneimage convert input.png output.jpg --quality 85
```

### Debug Mode Conversion

Convert with detailed logging:
```bash
oneimage --logging --log-level DEBUG convert input.png output.webp
```

## Development

### Setup Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/JuanS3/oneimage.git
   cd oneimage
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

```bash
pytest
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- pylint for linting
- mypy for type checking

Run all style checks:
```bash
black .
isort .
pylint oneimage
mypy oneimage
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/)
- Image processing powered by [Pillow](https://python-pillow.org/)
- Logging system uses [Loguru](https://github.com/Delgan/loguru)
- Terminal UI enhanced with [Rich](https://rich.readthedocs.io/)
