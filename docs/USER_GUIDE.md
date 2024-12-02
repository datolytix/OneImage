# OneImage User Guide

This guide provides detailed information about using OneImage, a command-line tool for image format conversion.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Advanced Features](#advanced-features)
4. [Troubleshooting](#troubleshooting)
5. [Best Practices](#best-practices)

## Installation

### System Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Sufficient disk space for image processing

### Installation Steps

1. Using pip:
   ```bash
   pip install oneimage
   ```

2. Verify installation:
   ```bash
   oneimage --version
   ```

## Basic Usage

### Simple Image Conversion

Convert an image from one format to another:

```bash
oneimage convert input.jpg output.webp
```

The tool automatically detects the input and output formats based on file extensions.

### Supported Formats

- **Input Formats:**
  - JPEG/JPG (`.jpg`, `.jpeg`)
  - PNG (`.png`)
  - WebP (`.webp`)

- **Output Formats:**
  - JPEG/JPG (`.jpg`, `.jpeg`)
  - PNG (`.png`)
  - WebP (`.webp`)

### Quality Control

For lossy formats (JPEG, WebP), you can control the output quality:

```bash
oneimage convert input.png output.jpg --quality 85
```

Quality settings:
- Range: 1-100
- Recommended: 70-90
- Default: Format-dependent

## Advanced Features

### Logging System

OneImage provides comprehensive logging capabilities:

1. **Enable Console Logging:**
   ```bash
   oneimage --logging convert input.png output.jpg
   ```

2. **Set Log Level:**
   ```bash
   oneimage --logging --log-level DEBUG convert input.png output.jpg
   ```

   Available levels:
   - DEBUG: Detailed debugging information
   - INFO: General operational information
   - WARNING: Warning messages
   - ERROR: Error messages only

3. **Log File Location:**
   - Default: `logs/oneimage.log`
   - Rotates automatically at 1MB
   - Keeps historical logs

### Shell Completion

Enable command completion for your shell:

```bash
# Bash
oneimage --install-completion bash

# Zsh
oneimage --install-completion zsh

# Fish
oneimage --install-completion fish
```

## Troubleshooting

### Common Issues

1. **"File not found" error:**
   - Check if the input file exists
   - Verify file permissions
   - Use absolute paths if unsure

2. **"Unsupported format" error:**
   - Verify file extension matches actual format
   - Check if format is supported
   - Ensure file is not corrupted

3. **Quality issues:**
   - Increase quality setting for lossy formats
   - Use PNG for lossless requirements
   - Check input image quality

### Error Messages

Common error messages and their solutions:

| Error Message | Possible Cause | Solution |
|--------------|----------------|-----------|
| "File not found" | Input file missing | Check file path |
| "Permission denied" | Insufficient permissions | Check file/directory permissions |
| "Invalid quality value" | Quality outside 1-100 | Use value between 1-100 |
| "Unsupported format" | Format not supported | Use supported format |

## Best Practices

### Image Quality

1. **Choosing Output Format:**
   - Use PNG for:
     - Screenshots
     - Images with text
     - Images requiring transparency
   - Use JPEG for:
     - Photos
     - Large images where size is important
   - Use WebP for:
     - Web content
     - Best balance of quality and size

2. **Quality Settings:**
   - JPEG:
     - 80-90 for high quality
     - 60-75 for web content
   - WebP:
     - 75-85 for general use
     - 85-95 for high quality

### Performance

1. **Large Files:**
   - Enable logging for progress tracking
   - Use appropriate quality settings
   - Consider batch processing for multiple files

2. **Batch Processing:**
   - Process similar images with same settings
   - Use consistent naming conventions
   - Monitor disk space

### File Management

1. **Naming Conventions:**
   - Use descriptive names
   - Include format in filename
   - Avoid spaces in filenames

2. **Directory Organization:**
   - Keep source images separate
   - Use subdirectories for different formats
   - Maintain backup of original files

## Support

For additional support:
1. Check the [GitHub repository](https://github.com/JuanS3/oneimage)
2. Review logged errors in `logs/oneimage.log`
3. Open an issue on GitHub for bugs or feature requests
