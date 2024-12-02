"""Command-line interface for OneImage."""

import os
import sys
from enum import Enum
from pathlib import Path
from typing import Optional, Annotated

import typer
from loguru import logger
from rich import print
from rich.console import Console
from rich.panel import Panel

from ..core.converter import ImageConverter
from ..utils.validators import ValidationError
from ..config.settings import (
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_ROTATION,
    SUPPORTED_FORMATS,
)


# Create Typer app instance
app = typer.Typer(
    name="oneimage",
    help="A command-line tool for image format conversion and manipulation",
    add_completion=True,
)

# Create console for rich output
console = Console()


class LogLevel(str, Enum):
    """Log level options."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


def setup_logging(show_logs: bool = False, log_level: LogLevel = LogLevel.INFO) -> None:
    """
    Configure logging for the application.

    Parameters
    ----------
    show_logs : bool, optional
        Whether to show logs in console output, by default False
    log_level : LogLevel, optional
        The logging level to use, by default LogLevel.INFO
    """
    # Remove default logger
    logger.remove()

    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)

    # Define log formats
    file_format = DEFAULT_LOG_FORMAT
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>\n"
        "{exception}"
    )

    # Always log to file with default format
    logger.add(
        "logs/oneimage.log",
        rotation=DEFAULT_LOG_ROTATION,
        level=log_level,
        format=file_format,
        backtrace=True,
        diagnose=True,
    )

    # Add console logger with colors if enabled
    if show_logs:
        logger.add(
            sys.stderr,
            level=log_level,
            format=console_format,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )


def version_callback(value: bool):
    """Show version information."""
    if value:
        from .. import __version__
        print(Panel.fit(
            f"[bold blue]OneImage[/bold blue] version: [green]{__version__}[/green]",
            title="Version Info"
        ))
        raise typer.Exit()


@app.callback()
def main(
    logging: Annotated[
        bool, typer.Option(
            "--logging", "-l",
            help="Enable console logging output",
            show_default=True,
        )
    ] = False,
    log_level: Annotated[
        LogLevel, typer.Option(
            "--log-level",
            help="Set the logging level",
            case_sensitive=False,
            show_default=True,
        )
    ] = LogLevel.INFO,
    version: Annotated[
        bool, typer.Option(
            "--version", "-v",
            help="Show version information and exit",
            callback=version_callback,
            is_eager=True,
        )
    ] = False,
) -> None:
    """
    OneImage - Command-line tool for image format conversion.

    This tool provides functionality to convert images between different formats
    while maintaining image quality and proper error handling.
    """
    setup_logging(show_logs=logging, log_level=log_level)


@app.command()
def convert(
    input_file: Annotated[
        Path, typer.Argument(
            help="Path to the input image file",
            exists=True,
            dir_okay=False,
            resolve_path=True,
        )
    ],
    output_file: Annotated[
        Path, typer.Argument(
            help="Path where the converted image will be saved",
            dir_okay=False,
            resolve_path=True,
        )
    ],
    quality: Annotated[
        Optional[int], typer.Option(
            "--quality", "-q",
            help="Output image quality (1-100)",
            min=1,
            max=100,
        )
    ] = None,
) -> None:
    """Convert an image from one format to another."""
    try:
        # Validate output format
        if output_file.suffix.lower() not in SUPPORTED_FORMATS:
            supported_formats_str = ', '.join(sorted(SUPPORTED_FORMATS))
            raise ValidationError(
                f"Unsupported output format. Supported formats: {supported_formats_str}"
            )

        # Validate paths
        from ..utils.validators import validate_image_path, validate_quality
        validate_image_path(input_file, should_exist=True)
        validate_image_path(output_file, should_exist=False)

        # Validate quality if provided
        if quality is not None:
            validate_quality(quality)

        # Show progress
        with console.status(f"Converting {input_file.name} to {output_file.name}..."):
            # Convert the image
            ImageConverter.convert_image(input_file, output_file, quality)

        # Show success message
        print(Panel.fit(
            f"[green]Successfully converted[/green] [bold]{input_file.name}[/bold] to [bold]{output_file.name}[/bold]",
            title="Success"
        ))

    except ValidationError as e:
        logger.error(str(e))
        print(Panel.fit(
            f"[red]Error:[/red] {str(e)}",
            title="Error",
            border_style="red"
        ))
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(Panel.fit(
            f"[red]Unexpected error:[/red] {str(e)}",
            title="Error",
            border_style="red"
        ))
        sys.exit(1)


if __name__ == '__main__':
    app()
