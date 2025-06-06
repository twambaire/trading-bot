import pandas as pd
import numpy as np
from typing import Dict, Optional

from app.backtester.strategies.base import Strategy

class RSIStrategy(Strategy):
    """
    A Relative Strength Index (RSI) strategy.
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
                "window": 14,
                "oversold": 30,
                "overbought": 70,
            }
    
    def generate_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate trading signals based on RSI.
        
        Args:
            data: The market data
            
        Returns:
            A dictionary with trading signals
        """
        signals = {}
        
        # Get parameters
        window = self.parameters.get("window", 14)
        oversold = self.parameters.get("oversold", 30)
        overbought = self.parameters.get("overbought", 70)
        
        # Check if we have enough data
        if len(data) < window + 1:
            return signals
        
        # Calculate RSI
        delta = data["close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Generate signals
        if rsi.iloc[-1] < oversold and rsi.iloc[-2] >= oversold:
            signals["action"] = "buy"
            signals["quantity"] = 1
        elif rsi.iloc[-1] > overbought and rsi.iloc[-2] <= overbought:
            signals["action"] = "sell"
        
        return signals

