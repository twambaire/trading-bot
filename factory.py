from typing import Dict, Optional

from app.backtester.strategies.base import Strategy
from app.backtester.strategies.moving_average import MovingAverageStrategy
from app.backtester.strategies.rsi import RSIStrategy

class StrategyFactory:
    """
    Factory for creating strategy instances.
    """
    
    @staticmethod
    def create_strategy(strategy_type: str, parameters: Dict = None) -> Strategy:
        """
        Create a strategy instance.
        
        Args:
            strategy_type: The type of strategy
            parameters: The strategy parameters
            
        Returns:
            A strategy instance
        """
        if strategy_type == "moving_average":
            return MovingAverageStrategy(parameters)
        elif strategy_type == "rsi":
            return RSIStrategy(parameters)
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

