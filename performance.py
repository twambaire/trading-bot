import pandas as pd
import numpy as np
from typing import Dict

def calculate_performance(equity_curve: pd.DataFrame) -> Dict:
    """
    Calculate performance metrics from an equity curve.
    
    Args:
        equity_curve: The equity curve
        
    Returns:
        A dictionary with performance metrics
    """
    # Calculate returns
    equity_curve["returns"] = equity_curve["equity"].pct_change()
    returns = equity_curve["returns"].dropna()
    
    # Calculate metrics
    total_return = (equity_curve["equity"].iloc[-1] / equity_curve["equity"].iloc[0]) - 1
    
    # Annualized return (assuming 252 trading days per year)
    days = (equity_curve["date"].iloc[-1] - equity_curve["date"].iloc[0]).days
    annual_return = (1 + total_return) ** (252 / max(days, 1)) - 1
    
    # Volatility (annualized)
    volatility = returns.std() * np.sqrt(252)
    
    # Sharpe ratio (assuming risk-free rate of 0)
    sharpe_ratio = annual_return / volatility if volatility != 0 else 0
    
    # Calculate drawdown
    equity_curve["drawdown"] = 1 - equity_curve["equity"] / equity_curve["equity"].cummax()
    max_drawdown = equity_curve["drawdown"].max()
    
    # Calculate win rate
    win_rate = len(returns[returns > 0]) / len(returns) if len(returns) > 0 else 0
    
    # Calculate profit factor
    gross_profit = returns[returns > 0].sum()
    gross_loss = abs(returns[returns < 0].sum())
    profit_factor = gross_profit / gross_loss if gross_loss != 0 else float("inf")
    
    return {
        "total_return": total_return,
        "annual_return": annual_return,
        "volatility": volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
    }

