import pandas as pd
import numpy as np
from typing import Dict, Optional

from app.backtester.strategies.base import Strategy

class MovingAverageStrategy(Strategy):
    """
    A simple moving average crossover strategy.
    """
    
    def __init__(self, parameters: Dict = None):
        """
        Initialize the strategy.
        
        Args:
            parameters: Strategy parameters
        """
        super().__init__(parameters)
        
        # Set default parameters if not provided
        if not self.parameters:
            self.parameters = {
                "short_window": 50,
                "long_window": 200,
            }
    
    def generate_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate trading signals based on moving average crossover.
        
        Args:
            data: The market data
            
        Returns:
            A dictionary with trading signals
        """
        signals = {}
        
        # Get parameters
        short_window = self.parameters.get("short_window", 50)
        long_window = self.parameters.get("long_window", 200)
        
        # Check if we have enough data
        if len(data) < long_window:
            return signals
        
        # Calculate moving averages
        short_ma = data["close"].rolling(window=short_window).mean()
        long_ma = data["close"].rolling(window=long_window).mean()
        
        # Generate signals
        if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] <= long_ma.iloc[-2]:
            signals["action"] = "buy"
            signals["quantity"] = 1
        elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
            signals["action"] = "sell"
        
        return signals

