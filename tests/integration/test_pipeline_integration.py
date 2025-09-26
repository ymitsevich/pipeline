"""Integration tests for the complete pipeline."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from pipeline.core.pipeline import Pipeline
from pipeline.config.settings import Settings
from pipeline.data.processor import PandasProcessor


@pytest.mark.integration
class TestPipelineIntegration:
    """Integration test cases for the complete pipeline."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_pipeline_execution(self, test_settings: Settings, sample_batch_data: list):
        """Test complete end-to-end pipeline execution."""
        # Create pipeline with test settings
        pipeline = Pipeline(config=test_settings)
        
        # Execute pipeline with sample data
        result = await pipeline.run(sample_batch_data)
        
        # Verify results
        assert result["status"] == "success"
        assert result["processed_records"] == len(sample_batch_data)
        assert isinstance(result["config"], dict)
    
    @pytest.mark.asyncio
    async def test_pipeline_with_data_processor(self, test_settings: Settings, sample_batch_data: list):
        """Test pipeline integration with data processor."""
        # Initialize components
        pipeline = Pipeline(config=test_settings)
        processor = PandasProcessor()
        
        # Process data first
        processed_df = processor.process(sample_batch_data)
        
        # Convert back to dict for pipeline
        processed_data = processed_df.to_dict('records')
        
        # Execute pipeline
        result = await pipeline.run(processed_data)
        
        # Verify results
        assert result["status"] == "success"
        assert result["processed_records"] == len(processed_data)
    
    @pytest.mark.asyncio
    async def test_pipeline_error_handling(self, test_settings: Settings, mocker):
        """Test pipeline error handling in integration scenario."""
        pipeline = Pipeline(config=test_settings)
        
        # Mock internal method to simulate error
        mocker.patch.object(
            pipeline,
            '_execute_pipeline',
            side_effect=Exception("Integration test error")
        )
        
        # Verify error is properly handled
        with pytest.raises(Exception, match="Integration test error"):
            await pipeline.run({})
    
    @pytest.mark.asyncio
    async def test_multiple_pipeline_instances(self, test_settings: Settings):
        """Test running multiple pipeline instances concurrently."""
        # Create multiple pipeline instances
        pipeline1 = Pipeline(config=test_settings)
        pipeline2 = Pipeline(config=test_settings)
        
        # Run pipelines concurrently
        results = await asyncio.gather(
            pipeline1.run({"instance": "1"}),
            pipeline2.run({"instance": "2"})
        )
        
        # Verify both completed successfully
        assert len(results) == 2
        assert all(result["status"] == "success" for result in results)
        assert results[0]["processed_records"] == 1
        assert results[1]["processed_records"] == 1
    
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_pipeline_performance_with_large_dataset(self, test_settings: Settings):
        """Test pipeline performance with larger dataset."""
        # Create larger dataset
        large_dataset = [
            {"id": f"test-{i}", "value": i, "batch": "performance_test"}
            for i in range(1000)
        ]
        
        pipeline = Pipeline(config=test_settings)
        
        # Measure execution time
        import time
        start_time = time.time()
        
        result = await pipeline.run(large_dataset)
        
        execution_time = time.time() - start_time
        
        # Verify results and performance
        assert result["status"] == "success"
        assert result["processed_records"] == len(large_dataset)
        assert execution_time < 10.0  # Should complete within 10 seconds
