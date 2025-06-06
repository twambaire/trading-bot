import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime

class Portfolio:
    """
    Manages a simulated portfolio for backtesting.
    """
    
    def __init__(self, initial_capital: float = 10000.0):
        """
        Initialize the portfolio.
        
        Args:
            initial_capital: The initial capital
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions = {}
        self.equity_curve = []
        self.trades = []
    
    def update(
        self,
        bar: pd.Series,
        signals: Dict,
        commission: float = 0.0,
        slippage: float = 0.0,
    ):
        """
        Update the portfolio based on signals.
        
        Args:
            bar: The current price bar
            signals: The trading signals
            commission: The commission per trade (percentage)
            slippage: The slippage per trade (percentage)
        """
        # Get current date and price
        date = bar["date"]
        price = bar["close"]
        symbol = bar.get("symbol", "Unknown")
        
        # Execute trades based on signals
        if "action" in signals:
            action = signals["action"]
            
            if action == "buy" and "quantity" in signals:
                # Calculate actual execution price with slippage
                execution_price = price * (1 + slippage)
                
                # Calculate commission
                quantity = signals["quantity"]
                commission_amount = execution_price * quantity * commission
                
                # Check if we have enough cash
                cost = execution_price * quantity + commission_amount
                
                if cost <= self.cash:
                    # Execute buy order
                    self.positions[symbol] = {
                        "quantity": quantity,
                        "price": execution_price,
                    }
                    
                    # Update cash
                    self.cash -= cost
                    
                    # Record trade
                    self.trades.append({
                        "date": date,
                        "symbol": symbol,
                        "action": "buy",
                        "quantity": quantity,
                        "price": execution_price,
                        "commission": commission_amount,
                    })
            
            elif action == "sell" and symbol in self.positions:
                # Calculate actual execution price with slippage
                execution_price = price * (1 - slippage)
                
                # Get position details
                position = self.positions[symbol]
                quantity = position["quantity"]
                
                # Calculate commission
                commission_amount = execution_price * quantity * commission
                
                # Execute sell order
                proceeds = execution_price * quantity - commission_amount
                self.cash += proceeds
                
                # Record trade
                self.trades.append({
                    "date": date,
                    "symbol": symbol,
                    "action": "sell",
                    "quantity": quantity,
                    "price": execution_price,
                    "commission": commission_amount,
                })
                
                # Remove position
                del self.positions[symbol]
        
        # Calculate portfolio value
        portfolio_value = self.cash
        
        for symbol, position in self.positions.items():
            portfolio_value += position["quantity"] * price
        
        # Update equity curve
        self.equity_curve.append({
            "date": date,
            "equity": portfolio_value,
        })
    
    def get_equity_curve(self) -> pd.DataFrame:
        """
        Get the equity curve.
        
        Returns:
            A pandas DataFrame with the equity curve
        """
        return pd.DataFrame(self.equity_curve)
    
    def get_trades(self) -> pd.DataFrame:
        """
        Get the trades.
        
        Returns:
            A pandas DataFrame with the trades
        """
        return pd.DataFrame(self.trades)

