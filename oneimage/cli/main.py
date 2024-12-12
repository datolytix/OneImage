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
from ..core.watermark import WatermarkProcessor
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


@app.command()
def resize(
    input_file: Path = typer.Argument(..., help="Input image file path"),
    output_file: Path = typer.Argument(..., help="Output image file path"),
    width: Optional[int] = typer.Option(None, "--width", "-w", help="Target width in pixels"),
    height: Optional[int] = typer.Option(None, "--height", "-h", help="Target height in pixels"),
    maintain_aspect_ratio: bool = typer.Option(True, "--no-aspect-ratio", help="Don't maintain aspect ratio", show_default=False),
    quality: Optional[int] = typer.Option(None, "--quality", "-q", help="Output image quality (1-100)"),
    show_logs: bool = typer.Option(False, "--show-logs", help="Show detailed logs"),
    log_level: LogLevel = typer.Option(LogLevel.INFO, "--log-level", help="Log level"),
) -> None:
    """
    Resize an image to specified dimensions.

    If only width or height is specified, the other dimension will be calculated to maintain aspect ratio.
    If both dimensions are specified and --no-aspect-ratio is not used, the image will be resized to fit
    within the specified dimensions while maintaining aspect ratio.
    """
    try:
        # Setup logging
        setup_logging(show_logs, log_level)
        logger.debug("Starting resize command")

        # Show resize operation details
        console.print(Panel.fit(
            f"[bold]Resize Operation[/bold]\n"
            f"Input: [cyan]{input_file}[/cyan]\n"
            f"Output: [cyan]{output_file}[/cyan]\n"
            f"Width: [cyan]{width or 'auto'}[/cyan]\n"
            f"Height: [cyan]{height or 'auto'}[/cyan]\n"
            f"Maintain Aspect Ratio: [cyan]{maintain_aspect_ratio}[/cyan]",
            title="OneImage",
            border_style="blue"
        ))

        with console.status(f"Resizing {input_file.name} to {output_file.name}..."):
            # Resize the image
            ImageConverter.resize_image(
                input_file,
                output_file,
                width=width,
                height=height,
                maintain_aspect_ratio=maintain_aspect_ratio,
                quality=quality
            )

        # Show success message
        print(Panel.fit(
            f"[green]Successfully resized[/green] [bold]{input_file.name}[/bold] to [bold]{output_file.name}[/bold]",
            title="Success",
            border_style="green"
        ))

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        console.print("[red]An unexpected error occurred[/red]")
        if show_logs:
            console.print(f"[red]Error details:[/red] {str(e)}")
        sys.exit(1)


@app.command()
def rotate(
    input_path: Path = typer.Argument(..., help="Path to input image"),
    output_path: Path = typer.Argument(..., help="Path for output image"),
    angle: float = typer.Option(90.0, help="Rotation angle in degrees (counter-clockwise)"),
    expand: bool = typer.Option(True, help="Expand output to fit rotated image"),
    quality: Optional[int] = typer.Option(None, help="Quality for lossy formats (1-100)"),
    log_level: str = typer.Option("INFO", help="Logging level"),
):
    """
    Rotate an image by a specified angle.
    """
    try:
        setup_logging(log_level)
        logger.debug(f"Starting rotation with angle {angle}")

        converter = ImageConverter()
        converter.rotate_image(
            input_path=input_path,
            output_path=output_path,
            angle=angle,
            expand=expand,
            quality=quality,
        )

        console.print(f"[green]Successfully rotated image:[/] {input_path} -> {output_path}")

    except ValidationError as e:
        console.print(f"[red]Validation error:[/] {str(e)}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/] {str(e)}")
        raise typer.Exit(1)


@app.command()
def watermark(
    input_path: Path = typer.Argument(..., help="Path to input image"),
    output_path: Path = typer.Argument(..., help="Path for output image"),
    text: str = typer.Option(..., help="Text to use as watermark"),
    position: str = typer.Option(
        "bottom-right",
        help="Watermark position (top-left, top-right, bottom-left, bottom-right, center)"
    ),
    opacity: int = typer.Option(50, help="Watermark opacity (0-100)"),
    font_size: int = typer.Option(36, help="Font size for watermark text"),
    font_color: str = typer.Option("white", help="Color of watermark text"),
    quality: Optional[int] = typer.Option(None, help="Quality for lossy formats (1-100)"),
    log_level: str = typer.Option("INFO", help="Logging level"),
):
    """
    Add a text watermark to an image.
    """
    try:
        setup_logging(show_logs=True, log_level=log_level)
        logger.debug(f"Adding watermark to {input_path}")

        WatermarkProcessor.add_watermark(
            input_path=input_path,
            output_path=output_path,
            text=text,
            position=position,
            opacity=opacity,
            font_size=font_size,
            font_color=font_color,
            quality=quality,
        )

        console.print(f"[green]Successfully added watermark:[/] {input_path} -> {output_path}")

    except ValidationError as e:
        console.print(f"[red]Validation error:[/] {str(e)}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/] {str(e)}")
        raise typer.Exit(1)


@app.command()
def remove_bg(
    input_path: Path = typer.Argument(..., help="Path to input image"),
    output_path: Path = typer.Argument(..., help="Path for output image"),
    model: str = typer.Option("u2net", help="Model to use for background removal (u2net, u2netp, u2net_human_seg)"),
    alpha_matting: bool = typer.Option(False, help="Use alpha matting for better edge detection"),
    alpha_matting_foreground_threshold: int = typer.Option(240, help="Alpha matting foreground threshold"),
    alpha_matting_background_threshold: int = typer.Option(10, help="Alpha matting background threshold"),
    alpha_matting_erode_size: int = typer.Option(10, help="Alpha matting erode size"),
    quality: Optional[int] = typer.Option(None, help="Quality for lossy formats (1-100)"),
    log_level: str = typer.Option("INFO", help="Logging level"),
):
    """
    Remove the background from an image.

    This command uses AI to detect and remove the background from images,
    leaving only the main subject. Perfect for product photos or portraits.
    """
    try:
        setup_logging(show_logs=True, log_level=log_level)
        logger.debug(f"Removing background from {input_path}")

        from ..core.background import BackgroundRemover

        remover = BackgroundRemover()
        result = remover.remove_background(
            str(input_path),
            model_name=model,
            alpha_matting=alpha_matting,
            alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
            alpha_matting_background_threshold=alpha_matting_background_threshold,
            alpha_matting_erode_size=alpha_matting_erode_size,
        )

        # Save the image with the specified quality
        result.save(
            str(output_path),
            quality=quality if quality is not None else 95
        )

        console.print(
            Panel(
                f"✨ Successfully removed background and saved to: [bold green]{output_path}[/bold green]",
                title="Success",
                style="green",
            )
        )

    except Exception as e:
        logger.error(f"Error removing background: {str(e)}")
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


if __name__ == '__main__':
    app()
