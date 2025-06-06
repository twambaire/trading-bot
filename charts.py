import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Optional
import io
import base64
from datetime import datetime

def create_equity_curve_chart(equity_curve: pd.DataFrame) -> str:
    """
    Create an equity curve chart.
    
    Args:
        equity_curve: The equity curve
        
    Returns:
        A base64-encoded PNG image
    """
    # Convert date strings to datetime if needed
    if isinstance(equity_curve["date"].iloc[0], str):
        equity_curve["date"] = pd.to_datetime(equity_curve["date"])
    
    # Set up the figure
    plt.figure(figsize=(10, 6))
    
    # Plot equity curve
    plt.plot(equity_curve["date"], equity_curve["equity"])
    
    # Add labels and title
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.title("Equity Curve")
    
    # Add grid
    plt.grid(True)
    
    # Format x-axis dates
    plt.gcf().autofmt_xdate()
    
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    # Encode the buffer as base64
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    
    # Close the figure
    plt.close()
    
    return img_str

def create_drawdown_chart(equity_curve: pd.DataFrame) -> str:
    """
    Create a drawdown chart.
    
    Args:
        equity_curve: The equity curve
        
    Returns:
        A base64-encoded PNG image
    """
    # Convert date strings to datetime if needed
    if isinstance(equity_curve["date"].iloc[0], str):
        equity_curve["date"] = pd.to_datetime(equity_curve["date"])
    
    # Calculate drawdown
    equity_curve["drawdown"] = 1 - equity_curve["equity"] / equity_curve["equity"].cummax()
    
    # Set up the figure
    plt.figure(figsize=(10, 6))
    
    # Plot drawdown
    plt.plot(equity_curve["date"], equity_curve["drawdown"])
    
    # Add labels and title
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.title("Drawdown")
    
    # Add grid
    plt.grid(True)
    
    # Format x-axis dates
    plt.gcf().autofmt_xdate()
    
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    # Encode the buffer as base64
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    
    # Close the figure
    plt.close()
    
    return img_str

def create_returns_distribution_chart(equity_curve: pd.DataFrame) -> str:
    """
    Create a returns distribution chart.
    
    Args:
        equity_curve: The equity curve
        
    Returns:
        A base64-encoded PNG image
    """
    # Convert date strings to datetime if needed
    if isinstance(equity_curve["date"].iloc[0], str):
        equity_curve["date"] = pd.to_datetime(equity_curve["date"])
    
    # Calculate returns
    equity_curve["returns"] = equity_curve["equity"].pct_change()
    
    # Set up the figure
    plt.figure(figsize=(10, 6))
    
    # Plot returns distribution
    sns.histplot(equity_curve["returns"].dropna(), kde=True)
    
    # Add labels and title
    plt.xlabel("Returns")
    plt.ylabel("Frequency")
    plt.title("Returns Distribution")
    
    # Add grid
    plt.grid(True)
    
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    # Encode the buffer as base64
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    
    # Close the figure
    plt.close()
    
    return img_str

def create_trades_chart(data: pd.DataFrame, trades: pd.DataFrame) -> str:
    """
    Create a chart showing trades on price data.
    
    Args:
        data: The market data
        trades: The trades
        
    Returns:
        A base64-encoded PNG image
    """
    # Convert date strings to datetime if needed
    if isinstance(data["date"].iloc[0], str):
        data["date"] = pd.to_datetime(data["date"])
    if isinstance(trades["date"].iloc[0], str):
        trades["date"] = pd.to_datetime(trades["date"])
    
    # Set up the figure
    plt.figure(figsize=(12, 6))
    
    # Plot price data
    plt.plot(data["date"], data["close"], label="Close Price")
    
    # Plot buy trades
    buy_trades = trades[trades["action"] == "buy"]
    plt.scatter(buy_trades["date"], buy_trades["price"], color="green", marker="^", s=100, label="Buy")
    
    # Plot sell trades
    sell_trades = trades[trades["action"] == "sell"]
    plt.scatter(sell_trades["date"], sell_trades["price"], color="red", marker="v", s=100, label="Sell")
    
    # Add labels and title
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Trades")
    
    # Add legend
    plt.legend()
    
    # Add grid
    plt.grid(True)
    
    # Format x-axis dates
    plt.gcf().autofmt_xdate()
    
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    # Encode the buffer as base64
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    
    # Close the figure
    plt.close()
    
    return img_str

