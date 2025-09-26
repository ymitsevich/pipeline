"""Data processing utilities."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
import pandas as pd
import structlog

logger = structlog.get_logger()


class DataProcessor(ABC):
    """Abstract base class for data processors."""
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process the input data.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data
        """
        pass


class PandasProcessor(DataProcessor):
    """Data processor using pandas."""
    
    def __init__(self) -> None:
        """Initialize the pandas processor."""
        self.logger = logger.bind(processor="pandas")
    
    def process(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Process data using pandas.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Processed DataFrame
        """
        self.logger.info("Processing data with pandas")
        
        # Convert input to DataFrame if it's not already
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")
        
        # Basic processing example
        df = self._clean_data(df)
        df = self._transform_data(df)
        
        self.logger.info("Data processing completed", rows=len(df))
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the data."""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.fillna("")
        
        return df
    
    def _transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform the data."""
        # Add processing timestamp
        df["processed_at"] = pd.Timestamp.now()
        
        return df
