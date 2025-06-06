import pandas as pd
import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime

class DataFetcher:
    """
    Fetches historical market data from various sources.
    """
    
    def fetch_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Fetch historical data for a symbol.
        
        Args:
            symbol: The symbol to fetch data for
            start_date: The start date
            end_date: The end date
            interval: The data interval (e.g., "1d", "1h", "5m")
            
        Returns:
            A pandas DataFrame with the historical data
        """
        data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        
        # Reset index to make Date a column
        data = data.reset_index()
        
        # Rename columns to standard format
        data = data.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume"
        })
        
        return data

    def fetch_multiple_data(
        self,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical data for multiple symbols.
        
        Args:
            symbols: The symbols to fetch data for
            start_date: The start date
            end_date: The end date
            interval: The data interval (e.g., "1d", "1h", "5m")
            
        Returns:
            A dictionary mapping symbols to pandas DataFrames
        """
        data = {}
        for symbol in symbols:
            data[symbol] = self.fetch_data(symbol, start_date, end_date, interval)
        return data

