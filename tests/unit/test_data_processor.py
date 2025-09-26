"""Unit tests for data processor module."""

import pytest
import pandas as pd
from unittest.mock import Mock

from pipeline.data.processor import DataProcessor, PandasProcessor


@pytest.mark.unit
class TestPandasProcessor:
    """Test cases for PandasProcessor class."""
    
    def test_processor_initialization(self):
        """Test processor initialization."""
        processor = PandasProcessor()
        assert processor.logger is not None
    
    def test_process_with_dict(self, sample_data: dict):
        """Test processing with dictionary input."""
        processor = PandasProcessor()
        result = processor.process(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert "processed_at" in result.columns
    
    def test_process_with_list(self, sample_batch_data: list):
        """Test processing with list input."""
        processor = PandasProcessor()
        result = processor.process(sample_batch_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_batch_data)
        assert "processed_at" in result.columns
    
    def test_process_with_dataframe(self, sample_batch_data: list):
        """Test processing with DataFrame input."""
        processor = PandasProcessor()
        input_df = pd.DataFrame(sample_batch_data)
        
        result = processor.process(input_df)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_batch_data)
        assert "processed_at" in result.columns
        # Should not modify original dataframe
        assert "processed_at" not in input_df.columns
    
    def test_process_with_invalid_input(self):
        """Test processing with invalid input type."""
        processor = PandasProcessor()
        
        with pytest.raises(ValueError, match="Unsupported data type"):
            processor.process("invalid input")
    
    def test_clean_data_removes_duplicates(self):
        """Test that clean_data removes duplicate rows."""
        processor = PandasProcessor()
        
        # Create DataFrame with duplicates
        data = [
            {"id": 1, "name": "test"},
            {"id": 1, "name": "test"},  # duplicate
            {"id": 2, "name": "test2"}
        ]
        df = pd.DataFrame(data)
        
        cleaned_df = processor._clean_data(df)
        
        assert len(cleaned_df) == 2
        assert not cleaned_df.duplicated().any()
    
    def test_clean_data_handles_missing_values(self):
        """Test that clean_data handles missing values."""
        processor = PandasProcessor()
        
        # Create DataFrame with missing values
        data = [
            {"id": 1, "name": "test"},
            {"id": 2, "name": None},
            {"id": 3, "name": "test3"}
        ]
        df = pd.DataFrame(data)
        
        cleaned_df = processor._clean_data(df)
        
        # Missing values should be filled with empty string
        assert cleaned_df["name"].isna().sum() == 0
        assert cleaned_df.loc[1, "name"] == ""
    
    def test_transform_data_adds_timestamp(self, sample_batch_data: list):
        """Test that transform_data adds processed_at timestamp."""
        processor = PandasProcessor()
        df = pd.DataFrame(sample_batch_data)
        
        transformed_df = processor._transform_data(df)
        
        assert "processed_at" in transformed_df.columns
        assert not transformed_df["processed_at"].isna().any()
        
        # Check that timestamp is recent (within last minute)
        import pandas as pd
        now = pd.Timestamp.now()
        time_diff = now - transformed_df["processed_at"].iloc[0]
        assert time_diff.total_seconds() < 60
    
    def test_data_processor_abstract_class(self):
        """Test that DataProcessor is abstract and cannot be instantiated."""
        with pytest.raises(TypeError):
            DataProcessor()
