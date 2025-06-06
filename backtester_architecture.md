# Backtester Architecture

## Overview

The backtester module is a critical component of the trading bot system that allows users to test trading strategies on historical data. It simulates the execution of trading strategies and calculates performance metrics to evaluate their effectiveness. The backtester is designed to be modular, extensible, and efficient, capable of handling large datasets and complex strategies.

## Architecture Layers

### 1. Data Layer

The data layer is responsible for fetching, processing, and storing historical market data. It provides a clean interface for accessing data from various sources.

**Key Components:**
- **Data Fetcher**: Fetches historical data from various sources
- **Data Processor**: Processes and normalizes raw data
- **Data Storage**: Stores processed data for efficient access

### 2. Engine Layer

The engine layer is the core of the backtester, responsible for simulating the execution of trading strategies on historical data.

**Key Components:**
- **Backtest Engine**: Coordinates the backtesting process
- **Portfolio Manager**: Manages the simulated portfolio
- **Order Manager**: Simulates order execution
- **Performance Calculator**: Calculates performance metrics

### 3. Strategy Layer

The strategy layer defines the interface for trading strategies and provides implementations of common strategies.

**Key Components:**
- **Strategy Interface**: Defines the contract for trading strategies
- **Strategy Implementations**: Concrete implementations of trading strategies
- **Strategy Factory**: Creates strategy instances based on configuration

### 4. Visualization Layer

The visualization layer is responsible for generating charts and reports to visualize backtest results.

**Key Components:**
- **Chart Generator**: Generates charts for equity curves, drawdowns, etc.
- **Report Generator**: Generates detailed performance reports
- **Export Utilities**: Exports results to various formats

## Component Interactions

The following diagram illustrates how the different components interact with each other:

```
+----------------+      +----------------+      +----------------+
|                |      |                |      |                |
|  Data Layer    |----->|  Engine Layer  |----->|  Visualization |
|  (Fetch,       |      |  (Simulation,  |      |  Layer         |
|  Process,      |<-----|  Portfolio,    |<-----|  (Charts,      |
|  Store)        |      |  Performance)  |      |  Reports)      |
+----------------+      +----------------+      +----------------+
                                |
                                |
                                v
                        +----------------+
                        |                |
                        |  Strategy      |
                        |  Layer         |
                        |  (Algorithms)  |
                        +----------------+
```

1. The data layer fetches and processes historical data.
2. The engine layer uses the data to simulate the execution of trading strategies.
3. The strategy layer provides the trading logic to the engine layer.
4. The engine layer calculates performance metrics.
5. The visualization layer generates charts and reports based on the results.

## Backtester Module Structure

### Data Module

The data module is responsible for fetching, processing, and storing historical market data.

```python
# backtester/data/fetcher.py
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

# backtester/data/processor.py
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
        
        # Reset index if it's a DatetimeIndex
        if isinstance(processed_data.index, pd.DatetimeIndex):
            processed_data = processed_data.reset_index()
        
        # Ensure required columns exist
        required_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        for column in required_columns:
            if column not in processed_data.columns:
                if column == "Date" and "Datetime" in processed_data.columns:
                    processed_data = processed_data.rename(columns={"Datetime": "Date"})
                else:
                    raise ValueError(f"Required column {column} not found in data")
        
        # Ensure data is sorted by date
        processed_data = processed_data.sort_values("Date")
        
        # Remove duplicates
        processed_data = processed_data.drop_duplicates(subset=["Date"])
        
        # Fill missing values
        processed_data = processed_data.fillna(method="ffill")
        
        # Calculate additional features
        processed_data["Returns"] = processed_data["Close"].pct_change()
        
        return processed_data

# backtester/data/storage.py
import pandas as pd
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime

class DataStorage:
    """
    Stores and retrieves market data.
    """
    
    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize the data storage.
        
        Args:
            db_path: The path to the SQLite database
        """
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """
        Create the necessary tables.
        """
        cursor = self.conn.cursor()
        
        # Create symbols table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS symbols (
            id INTEGER PRIMARY KEY,
            symbol TEXT UNIQUE,
            name TEXT,
            exchange TEXT
        )
        """)
        
        # Create data table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY,
            symbol_id INTEGER,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            FOREIGN KEY (symbol_id) REFERENCES symbols (id),
            UNIQUE (symbol_id, date)
        )
        """)
        
        self.conn.commit()
    
    def store_data(self, symbol: str, data: pd.DataFrame):
        """
        Store market data for a symbol.
        
        Args:
            symbol: The symbol
            data: The market data
        """
        cursor = self.conn.cursor()
        
        # Insert or update symbol
        cursor.execute(
            "INSERT OR IGNORE INTO symbols (symbol) VALUES (?)",
            (symbol,)
        )
        
        # Get symbol ID
        cursor.execute("SELECT id FROM symbols WHERE symbol = ?", (symbol,))
        symbol_id = cursor.fetchone()[0]
        
        # Insert market data
        for _, row in data.iterrows():
            cursor.execute(
                """
                INSERT OR REPLACE INTO market_data
                (symbol_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    symbol_id,
                    row["Date"].strftime("%Y-%m-%d %H:%M:%S"),
                    row["Open"],
                    row["High"],
                    row["Low"],
                    row["Close"],
                    row["Volume"],
                )
            )
        
        self.conn.commit()
    
    def get_data(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> pd.DataFrame:
        """
        Get market data for a symbol.
        
        Args:
            symbol: The symbol
            start_date: The start date
            end_date: The end date
            
        Returns:
            A pandas DataFrame with the market data
        """
        cursor = self.conn.cursor()
        
        # Get symbol ID
        cursor.execute("SELECT id FROM symbols WHERE symbol = ?", (symbol,))
        result = cursor.fetchone()
        
        if result is None:
            return pd.DataFrame()
        
        symbol_id = result[0]
        
        # Build query
        query = """
        SELECT date, open, high, low, close, volume
        FROM market_data
        WHERE symbol_id = ?
        """
        params = [symbol_id]
        
        if start_date is not None:
            query += " AND date >= ?"
            params.append(start_date.strftime("%Y-%m-%d %H:%M:%S"))
        
        if end_date is not None:
            query += " AND date <= ?"
            params.append(end_date.strftime("%Y-%m-%d %H:%M:%S"))
        
        query += " ORDER BY date"
        
        # Execute query
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Create DataFrame
        data = pd.DataFrame(
            rows,
            columns=["Date", "Open", "High", "Low", "Close", "Volume"]
        )
        
        # Convert Date column to datetime
        data["Date"] = pd.to_datetime(data["Date"])
        
        return data
```

### Engine Module

The engine module is the core of the backtester, responsible for simulating the execution of trading strategies on historical data.

```python
# backtester/engine/backtest.py
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime

from app.backtester.strategies.base import Strategy
from app.backtester.engine.portfolio import Portfolio
from app.backtester.engine.performance import calculate_performance

class Backtest:
    """
    Backtests a trading strategy on historical data.
    """
    
    def __init__(
        self,
        strategy: Strategy,
        data: pd.DataFrame,
        initial_capital: float = 10000.0,
        commission: float = 0.0,
        slippage: float = 0.0,
    ):
        """
        Initialize the backtest.
        
        Args:
            strategy: The trading strategy to backtest
            data: The historical market data
            initial_capital: The initial capital
            commission: The commission per trade (percentage)
            slippage: The slippage per trade (percentage)
        """
        self.strategy = strategy
        self.data = data
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.portfolio = Portfolio(initial_capital)
        self.results = None
    
    def run(self) -> Dict:
        """
        Run the backtest.
        
        Returns:
            A dictionary with the backtest results
        """
        # Reset portfolio
        self.portfolio = Portfolio(self.initial_capital)
        
        # Run backtest
        for i in range(len(self.data)):
            # Get current data
            current_data = self.data.iloc[:i+1]
            current_bar = current_data.iloc[-1]
            
            # Generate signals
            signals = self.strategy.generate_signals(current_data)
            
            # Execute trades
            if signals:
                self.portfolio.update(
                    current_bar,
                    signals,
                    self.commission,
                    self.slippage
                )
        
        # Calculate performance metrics
        equity_curve = self.portfolio.get_equity_curve()
        trades = self.portfolio.get_trades()
        metrics = calculate_performance(equity_curve)
        
        # Store results
        self.results = {
            "equity_curve": equity_curve,
            "trades": trades,
            "metrics": metrics,
        }
        
        return self.results
    
    def get_results(self) -> Dict:
        """
        Get the backtest results.
        
        Returns:
            A dictionary with the backtest results
        """
        if self.results is None:
            self.run()
        
        return self.results

# backtester/engine/portfolio.py
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
        date = bar["Date"]
        price = bar["Close"]
        
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
                    self.positions[bar["symbol"]] = {
                        "quantity": quantity,
                        "price": execution_price,
                    }
                    
                    # Update cash
                    self.cash -= cost
                    
                    # Record trade
                    self.trades.append({
                        "date": date,
                        "symbol": bar["symbol"],
                        "action": "buy",
                        "quantity": quantity,
                        "price": execution_price,
                        "commission": commission_amount,
                    })
            
            elif action == "sell" and bar["symbol"] in self.positions:
                # Calculate actual execution price with slippage
                execution_price = price * (1 - slippage)
                
                # Get position details
                position = self.positions[bar["symbol"]]
                quantity = position["quantity"]
                
                # Calculate commission
                commission_amount = execution_price * quantity * commission
                
                # Execute sell order
                proceeds = execution_price * quantity - commission_amount
                self.cash += proceeds
                
                # Record trade
                self.trades.append({
                    "date": date,
                    "symbol": bar["symbol"],
                    "action": "sell",
                    "quantity": quantity,
                    "price": execution_price,
                    "commission": commission_amount,
                })
                
                # Remove position
                del self.positions[bar["symbol"]]
        
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

# backtester/engine/performance.py
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
    annual_return = (1 + total_return) ** (252 / len(returns)) - 1
    volatility = returns.std() * np.sqrt(252)
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
```

### Strategy Module

The strategy module defines the interface for trading strategies and provides implementations of common strategies.

```python
# backtester/strategies/base.py
import pandas as pd
from typing import Dict, Optional
from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    Base class for trading strategies.
    """
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate trading signals based on the data.
        
        Args:
            data: The market data
            
        Returns:
            A dictionary with trading signals
        """
        pass

# backtester/strategies/moving_average.py
import pandas as pd
import numpy as np
from typing import Dict, Optional

from app.backtester.strategies.base import Strategy

class MovingAverageStrategy(Strategy):
    """
    A simple moving average crossover strategy.
    """
    
    def __init__(self, short_window: int = 50, long_window: int = 200):
        """
        Initialize the strategy.
        
        Args:
            short_window: The short moving average window
            long_window: The long moving average window
        """
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate trading signals based on moving average crossover.
        
        Args:
            data: The market data
            
        Returns:
            A dictionary with trading signals
        """
        signals = {}
        
        # Check if we have enough data
        if len(data) < self.long_window:
            return signals
        
        # Calculate moving averages
        short_ma = data["Close"].rolling(window=self.short_window).mean()
        long_ma = data["Close"].rolling(window=self.long_window).mean()
        
        # Generate signals
        if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] <= long_ma.iloc[-2]:
            signals["action"] = "buy"
            signals["quantity"] = 1
        elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
            signals["action"] = "sell"
        
        return signals

# backtester/strategies/rsi.py
import pandas as pd
import numpy as np
from typing import Dict, Optional

from app.backtester.strategies.base import Strategy

class RSIStrategy(Strategy):
    """
    A Relative Strength Index (RSI) strategy.
    """
    
    def __init__(self, window: int = 14, oversold: float = 30, overbought: float = 70):
        """
        Initialize the strategy.
        
        Args:
            window: The RSI window
            oversold: The oversold threshold
            overbought: The overbought threshold
        """
        self.window = window
        self.oversold = oversold
        self.overbought = overbought
    
    def generate_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate trading signals based on RSI.
        
        Args:
            data: The market data
            
        Returns:
            A dictionary with trading signals
        """
        signals = {}
        
        # Check if we have enough data
        if len(data) < self.window + 1:
            return signals
        
        # Calculate RSI
        delta = data["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=self.window).mean()
        avg_loss = loss.rolling(window=self.window).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Generate signals
        if rsi.iloc[-1] < self.oversold and rsi.iloc[-2] >= self.oversold:
            signals["action"] = "buy"
            signals["quantity"] = 1
        elif rsi.iloc[-1] > self.overbought and rsi.iloc[-2] <= self.overbought:
            signals["action"] = "sell"
        
        return signals

# backtester/strategies/factory.py
from typing import Dict, Optional

from app.backtester.strategies.base import Strategy
from app.backtester.strategies.moving_average import MovingAverageStrategy
from app.backtester.strategies.rsi import RSIStrategy

class StrategyFactory:
    """
    Factory for creating strategy instances.
    """
    
    @staticmethod
    def create_strategy(strategy_type: str, parameters: Dict) -> Strategy:
        """
        Create a strategy instance.
        
        Args:
            strategy_type: The type of strategy
            parameters: The strategy parameters
            
        Returns:
            A strategy instance
        """
        if strategy_type == "moving_average":
            return MovingAverageStrategy(
                short_window=parameters.get("short_window", 50),
                long_window=parameters.get("long_window", 200),
            )
        elif strategy_type == "rsi":
            return RSIStrategy(
                window=parameters.get("window", 14),
                oversold=parameters.get("oversold", 30),
                overbought=parameters.get("overbought", 70),
            )
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
```

### Visualization Module

The visualization module is responsible for generating charts and reports to visualize backtest results.

```python
# backtester/visualization/charts.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Optional
import io
import base64

def create_equity_curve_chart(equity_curve: pd.DataFrame) -> str:
    """
    Create an equity curve chart.
    
    Args:
        equity_curve: The equity curve
        
    Returns:
        A base64-encoded PNG image
    """
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

# backtester/visualization/reports.py
import pandas as pd
from typing import Dict, Optional
import jinja2
import pdfkit

def create_performance_report(results: Dict) -> str:
    """
    Create a performance report.
    
    Args:
        results: The backtest results
        
    Returns:
        An HTML report
    """
    # Extract data
    equity_curve = results["equity_curve"]
    trades = results["trades"]
    metrics = results["metrics"]
    
    # Create Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
        autoescape=jinja2.select_autoescape(["html", "xml"])
    )
    
    # Load template
    template = env.get_template("performance_report.html")
    
    # Render template
    html = template.render(
        equity_curve=equity_curve,
        trades=trades,
        metrics=metrics,
    )
    
    return html

def create_pdf_report(html: str) -> bytes:
    """
    Create a PDF report from HTML.
    
    Args:
        html: The HTML report
        
    Returns:
        The PDF report as bytes
    """
    # Create PDF
    pdf = pdfkit.from_string(html, False)
    
    return pdf
```

## Backtester API

The backtester is exposed through a REST API that allows users to create and run backtests, as well as retrieve results.

```python
# api/endpoints/backtests.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_current_user, get_db
from app.schemas.backtest import Backtest, BacktestCreate, BacktestResults
from app.services.backtest import backtest_service
from app.db.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Backtest])
def get_backtests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all backtests for the current user.
    """
    return backtest_service.get_backtests(db, current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=Backtest)
def create_backtest(
    backtest_in: BacktestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new backtest.
    """
    return backtest_service.create_backtest(db, backtest_in, current_user.id)

@router.get("/{backtest_id}", response_model=Backtest)
def get_backtest(
    backtest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a backtest by ID.
    """
    backtest = backtest_service.get_backtest(db, backtest_id)
    if not backtest or backtest.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest

@router.delete("/{backtest_id}", response_model=Backtest)
def delete_backtest(
    backtest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a backtest.
    """
    backtest = backtest_service.get_backtest(db, backtest_id)
    if not backtest or backtest.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest_service.delete_backtest(db, backtest)

@router.get("/{backtest_id}/results", response_model=BacktestResults)
def get_backtest_results(
    backtest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get backtest results.
    """
    backtest = backtest_service.get_backtest(db, backtest_id)
    if not backtest or backtest.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Backtest not found")
    
    if not backtest.results:
        raise HTTPException(status_code=404, detail="Backtest results not found")
    
    return backtest.results

@router.get("/{backtest_id}/chart")
def get_backtest_chart(
    backtest_id: int,
    chart_type: str = "equity",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get backtest chart.
    """
    backtest = backtest_service.get_backtest(db, backtest_id)
    if not backtest or backtest.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Backtest not found")
    
    if not backtest.results:
        raise HTTPException(status_code=404, detail="Backtest results not found")
    
    # Generate chart
    if chart_type == "equity":
        from app.backtester.visualization.charts import create_equity_curve_chart
        chart = create_equity_curve_chart(backtest.results["equity_curve"])
    elif chart_type == "drawdown":
        from app.backtester.visualization.charts import create_drawdown_chart
        chart = create_drawdown_chart(backtest.results["equity_curve"])
    elif chart_type == "returns":
        from app.backtester.visualization.charts import create_returns_distribution_chart
        chart = create_returns_distribution_chart(backtest.results["equity_curve"])
    else:
        raise HTTPException(status_code=400, detail=f"Invalid chart type: {chart_type}")
    
    return {"chart": chart}
```

## Backtester Service

The backtester service is responsible for creating and running backtests, as well as storing and retrieving results.

```python
# services/backtest.py
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.models.backtest import Backtest
from app.db.models.strategy import Strategy
from app.schemas.backtest import BacktestCreate
from app.backtester.data.fetcher import DataFetcher
from app.backtester.strategies.factory import StrategyFactory
from app.backtester.engine.backtest import Backtest as BacktestEngine

class BacktestService:
    def get_backtests(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Backtest]:
        """
        Get all backtests for a user.
        """
        return db.query(Backtest).filter(Backtest.user_id == user_id).offset(skip).limit(limit).all()

    def get_backtest(self, db: Session, backtest_id: int) -> Optional[Backtest]:
        """
        Get a backtest by ID.
        """
        return db.query(Backtest).filter(Backtest.id == backtest_id).first()

    def create_backtest(
        self, db: Session, backtest_in: BacktestCreate, user_id: int
    ) -> Backtest:
        """
        Create a new backtest.
        """
        # Get strategy
        strategy_db = db.query(Strategy).filter(Strategy.id == backtest_in.strategy_id).first()
        if not strategy_db:
            raise ValueError(f"Strategy not found: {backtest_in.strategy_id}")
        
        # Create backtest
        backtest = Backtest(
            name=backtest_in.name,
            description=backtest_in.description,
            strategy_id=backtest_in.strategy_id,
            user_id=user_id,
            parameters=backtest_in.parameters,
            start_date=backtest_in.start_date,
            end_date=backtest_in.end_date,
            status="pending",
        )
        
        db.add(backtest)
        db.commit()
        db.refresh(backtest)
        
        # Run backtest
        try:
            # Update status
            backtest.status = "running"
            db.commit()
            
            # Fetch data
            data_fetcher = DataFetcher()
            data = data_fetcher.fetch_data(
                backtest_in.symbol,
                backtest_in.start_date,
                backtest_in.end_date,
            )
            
            # Create strategy
            strategy = StrategyFactory.create_strategy(
                strategy_db.type,
                {**strategy_db.parameters, **backtest_in.parameters},
            )
            
            # Run backtest
            backtest_engine = BacktestEngine(
                strategy=strategy,
                data=data,
                initial_capital=backtest_in.initial_capital,
                commission=backtest_in.commission,
                slippage=backtest_in.slippage,
            )
            
            results = backtest_engine.run()
            
            # Update backtest
            backtest.results = results
            backtest.status = "completed"
            db.commit()
            db.refresh(backtest)
        except Exception as e:
            # Update status
            backtest.status = "failed"
            backtest.error = str(e)
            db.commit()
            db.refresh(backtest)
            
            raise
        
        return backtest

    def delete_backtest(self, db: Session, backtest: Backtest) -> Backtest:
        """
        Delete a backtest.
        """
        db.delete(backtest)
        db.commit()
        return backtest

backtest_service = BacktestService()
```

## Conclusion

The backtester architecture is designed to be modular, extensible, and efficient. It provides a clean interface for testing trading strategies on historical data and calculating performance metrics. The modular design allows for easy addition of new data sources, strategies, and visualization methods. The backtester is integrated with the rest of the trading bot system through a REST API, allowing users to create and run backtests from the frontend.

