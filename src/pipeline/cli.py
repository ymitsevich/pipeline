"""Command-line interface for the pipeline application."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
import structlog

from pipeline.config.settings import get_settings
from pipeline.core.pipeline import Pipeline
from pipeline.utils.logging import configure_logging


@click.group()
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="Path to configuration file",
)
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.option("--log-level", default="INFO", help="Set logging level")
@click.pass_context
def main(ctx: click.Context, config: Optional[Path], debug: bool, log_level: str) -> None:
    """Pipeline application CLI."""
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Configure logging
    configure_logging(log_level=log_level, json_logs=not debug)
    logger = structlog.get_logger()
    
    # Load settings
    settings = get_settings()
    if debug:
        settings.debug = True
    
    # Store in context
    ctx.obj["settings"] = settings
    ctx.obj["logger"] = logger
    
    logger.info("Pipeline CLI initialized", environment=settings.environment)


@main.command()
@click.option(
    "--input-file",
    type=click.Path(exists=True, path_type=Path),
    help="Input data file",
)
@click.option("--dry-run", is_flag=True, help="Perform a dry run without executing")
@click.pass_context
def run(ctx: click.Context, input_file: Optional[Path], dry_run: bool) -> None:
    """Run the pipeline."""
    settings = ctx.obj["settings"]
    logger = ctx.obj["logger"]
    
    logger.info("Starting pipeline execution", dry_run=dry_run)
    
    if dry_run:
        logger.info("Dry run mode - pipeline would execute with settings", 
                   settings=settings.model_dump())
        return
    
    try:
        asyncio.run(_run_pipeline_async(settings, input_file, logger))
    except KeyboardInterrupt:
        logger.info("Pipeline execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error("Pipeline execution failed", error=str(e))
        sys.exit(1)


async def _run_pipeline_async(
    settings, 
    input_file: Optional[Path], 
    logger: structlog.BoundLoggerProtocol
) -> None:
    """Run the pipeline asynchronously."""
    pipeline = Pipeline(settings)
    
    # Load input data if provided
    input_data = {}
    if input_file:
        logger.info("Loading input data", file=str(input_file))
        # Here you would load your actual data
        # For now, just use a placeholder
        input_data = {"source_file": str(input_file)}
    
    # Execute pipeline
    result = await pipeline.run(input_data)
    logger.info("Pipeline completed successfully", result=result)


@main.command()
@click.pass_context
def config(ctx: click.Context) -> None:
    """Show current configuration."""
    settings = ctx.obj["settings"]
    
    click.echo("Current Configuration:")
    click.echo("=" * 50)
    
    config_dict = settings.model_dump()
    for key, value in config_dict.items():
        if isinstance(value, dict):
            click.echo(f"{key}:")
            for sub_key, sub_value in value.items():
                click.echo(f"  {sub_key}: {sub_value}")
        else:
            click.echo(f"{key}: {value}")


@main.command()
def health() -> None:
    """Check application health."""
    click.echo("Pipeline application is healthy ✓")


if __name__ == "__main__":
    main()
