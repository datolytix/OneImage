# OneImage User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Troubleshooting](#troubleshooting)
6. [Tips and Tricks](#tips-and-tricks)

## Introduction

OneImage is a command-line tool designed for efficient image manipulation. It provides three main functionalities:
- Format conversion between PNG, JPEG, and WebP
- Image resizing with aspect ratio control
- Image rotation with customizable angles

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Steps

1. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

2. Install OneImage:
   ```bash
   pip install -e .
   ```

## Basic Usage

### Format Conversion

The most basic use case is converting between image formats:

```bash
oneimage convert input.png output.jpg
```

For better quality JPEG or WebP output:
```bash
oneimage convert input.png output.jpg --quality 95
```

### Resizing Images

Resize while maintaining aspect ratio:
```bash
# By width
oneimage resize input.jpg output.jpg --width 800

# By height
oneimage resize input.jpg output.jpg --height 600
```

Exact dimensions (ignoring aspect ratio):
```bash
oneimage resize input.jpg output.jpg --width 800 --height 600 --no-aspect-ratio
```

### Rotating Images

Simple 90-degree rotation:
```bash
oneimage rotate input.jpg output.jpg
```

Custom angle with expanded canvas:
```bash
oneimage rotate input.png output.png --angle 45 --expand true
```

## Advanced Features

### Quality Control

The `--quality` parameter affects JPEG and WebP outputs:

- High quality (90-100): Minimal compression, larger files
- Medium quality (75-85): Good balance
- Low quality (60-75): Higher compression, smaller files

Example:
```bash
oneimage convert input.png output.jpg --quality 85
```

### Logging Levels

Control the verbosity of operation logs:

```bash
# Detailed debugging information
oneimage convert input.png output.jpg --log-level DEBUG

# Only warnings and errors
oneimage convert input.png output.jpg --log-level WARNING
```

Available levels:
- DEBUG: All information
- INFO: General operation info
- WARNING: Warnings and errors
- ERROR: Only errors

## Troubleshooting

### Common Issues

1. **"Invalid quality value"**
   - Ensure quality is between 1 and 100
   - Quality only applies to JPEG and WebP formats

2. **"File not found"**
   - Check if input file exists
   - Verify file permissions

3. **"Unsupported format"**
   - Verify input/output formats are PNG, JPEG, or WebP
   - Check file extensions match actual formats

4. **"Memory error"**
   - Try processing smaller images
   - Close other memory-intensive applications

### Error Messages

OneImage provides detailed error messages to help identify issues:

- Path validation errors
- Format compatibility issues
- Quality parameter problems
- File system errors

## Tips and Tricks

### Batch Processing

For multiple files, use shell loops:

```bash
# Convert all PNGs to JPG
for f in *.png; do
    oneimage convert "$f" "${f%.png}.jpg"
done
```

### Format Selection Guide

- **PNG**: Best for:
  - Screenshots
  - Images with text
  - Graphics with sharp edges
  - Images requiring transparency

- **JPEG**: Ideal for:
  - Photographs
  - Complex images with gradients
  - Web-optimized photos

- **WebP**: Good for:
  - Web graphics
  - Balanced quality/size ratio
  - Modern web applications

### Performance Optimization

1. **File Size**
   - Use appropriate quality settings
   - Choose suitable formats
   - Consider target use case

2. **Processing Speed**
   - Process in batches
   - Monitor system resources
   - Use appropriate logging levels

3. **Memory Usage**
   - Process large files individually
   - Close unnecessary applications
   - Monitor system memory

### Best Practices

1. **Workflow**
   - Organize input/output directories
   - Use meaningful filenames
   - Maintain original files

2. **Quality Settings**
   - Test different values
   - Document preferred settings
   - Consider end-use requirements

3. **Error Handling**
   - Check command output
   - Monitor log files
   - Back up important images
