import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class DataProcessor:
    """
    Processes raw market data.
    """
    
    def process_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Process raw market data.
        
        Args:
            data: The raw market data
            
        Returns:
            The processed market data
        """
        # Make a copy of the data
        processed_data = data.copy()
        
        # Ensure required columns exist
        required_columns = ["date", "open", "high", "low", "close", "volume"]
        for column in required_columns:
            if column not in processed_data.columns:
                raise ValueError(f"Required column {column} not found in data")
        
        # Ensure data is sorted by date
        processed_data = processed_data.sort_values("date")
        
        # Remove duplicates
        processed_data = processed_data.drop_duplicates(subset=["date"])
        
        # Fill missing values
        processed_data = processed_data.fillna(method="ffill")
        
        # Calculate additional features
        processed_data["returns"] = processed_data["close"].pct_change()
        
        return processed_data
    
    def add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add technical indicators to the data.
        
        Args:
            data: The market data
            
        Returns:
            The market data with technical indicators
        """
        # Make a copy of the data
        processed_data = data.copy()
        
        # Simple Moving Averages
        processed_data["sma_5"] = processed_data["close"].rolling(window=5).mean()
        processed_data["sma_10"] = processed_data["close"].rolling(window=10).mean()
        processed_data["sma_20"] = processed_data["close"].rolling(window=20).mean()
        processed_data["sma_50"] = processed_data["close"].rolling(window=50).mean()
        processed_data["sma_200"] = processed_data["close"].rolling(window=200).mean()
        
        # Exponential Moving Averages
        processed_data["ema_5"] = processed_data["close"].ewm(span=5, adjust=False).mean()
        processed_data["ema_10"] = processed_data["close"].ewm(span=10, adjust=False).mean()
        processed_data["ema_20"] = processed_data["close"].ewm(span=20, adjust=False).mean()
        processed_data["ema_50"] = processed_data["close"].ewm(span=50, adjust=False).mean()
        processed_data["ema_200"] = processed_data["close"].ewm(span=200, adjust=False).mean()
        
        # Bollinger Bands
        processed_data["bb_middle"] = processed_data["close"].rolling(window=20).mean()
        processed_data["bb_std"] = processed_data["close"].rolling(window=20).std()
        processed_data["bb_upper"] = processed_data["bb_middle"] + 2 * processed_data["bb_std"]
        processed_data["bb_lower"] = processed_data["bb_middle"] - 2 * processed_data["bb_std"]
        
        # RSI
        delta = processed_data["close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        
        rs = avg_gain / avg_loss
        processed_data["rsi"] = 100 - (100 / (1 + rs))
        
        # MACD
        processed_data["macd"] = processed_data["ema_12"] - processed_data["ema_26"]
        processed_data["macd_signal"] = processed_data["macd"].ewm(span=9, adjust=False).mean()
        processed_data["macd_histogram"] = processed_data["macd"] - processed_data["macd_signal"]
        
        return processed_data

