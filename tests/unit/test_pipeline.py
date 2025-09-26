"""Unit tests for the core pipeline module."""

import pytest
from unittest.mock import AsyncMock, Mock
import asyncio

from pipeline.core.pipeline import Pipeline
from pipeline.config.settings import Settings


@pytest.mark.unit
class TestPipeline:
    """Test cases for the Pipeline class."""
    
    def test_pipeline_initialization(self, test_settings: Settings):
        """Test pipeline initialization with settings."""
        pipeline = Pipeline(config=test_settings)
        
        assert pipeline.config == test_settings
        assert pipeline.logger is not None
    
    def test_pipeline_initialization_without_config(self):
        """Test pipeline initialization without explicit config."""
        pipeline = Pipeline()
        
        assert pipeline.config is not None
        assert isinstance(pipeline.config, Settings)
    
    @pytest.mark.asyncio
    async def test_pipeline_run_success(self, pipeline: Pipeline, sample_data: dict):
        """Test successful pipeline execution."""
        result = await pipeline.run(sample_data)
        
        assert result["status"] == "success"
        assert result["processed_records"] == len(sample_data)
        assert "config" in result
    
    @pytest.mark.asyncio
    async def test_pipeline_run_empty_data(self, pipeline: Pipeline):
        """Test pipeline execution with empty data."""
        result = await pipeline.run({})
        
        assert result["status"] == "success"
        assert result["processed_records"] == 0
    
    @pytest.mark.asyncio
    async def test_pipeline_run_no_data(self, pipeline: Pipeline):
        """Test pipeline execution with no data provided."""
        result = await pipeline.run()
        
        assert result["status"] == "success"
        assert result["processed_records"] == 0
    
    @pytest.mark.asyncio
    async def test_pipeline_run_with_exception(self, mocker, pipeline: Pipeline):
        """Test pipeline execution when an exception occurs."""
        # Mock the _execute_pipeline method to raise an exception
        mocker.patch.object(
            pipeline, 
            '_execute_pipeline', 
            side_effect=Exception("Test exception")
        )
        
        with pytest.raises(Exception, match="Test exception"):
            await pipeline.run({})
    
    @pytest.mark.asyncio
    async def test_execute_pipeline_internal(self, pipeline: Pipeline, sample_data: dict):
        """Test the internal _execute_pipeline method."""
        result = await pipeline._execute_pipeline(sample_data)
        
        assert result["status"] == "success"
        assert result["processed_records"] == len(sample_data)
        assert "config" in result
