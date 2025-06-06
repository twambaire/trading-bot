import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from app.backtester.strategies.base import BaseStrategy
from app.backtester.engine.backtest import Backtest
from app.backtester.engine.portfolio import Portfolio
from app.backtester.engine.performance import calculate_performance_metrics

# Create a simple test strategy
class TestStrategy(BaseStrategy):
    def __init__(self, parameters=None):
        super().__init__(parameters or {})
        self.name = "Test Strategy"
        self.description = "A simple test strategy"
    
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # Simple strategy: buy when price increases for 2 days, sell when it decreases for 2 days
        signals['price_change'] = data['close'].pct_change()
        signals['signal'][2:] = np.where(
            (signals['price_change'][1:-1] > 0) & (signals['price_change'][:-2] > 0),
            1.0,  # Buy signal
            np.where(
                (signals['price_change'][1:-1] < 0) & (signals['price_change'][:-2] < 0),
                -1.0,  # Sell signal
                0.0  # No signal
            )
        )
        
        return signals

# Create test data
def create_test_data():
    # Create a date range
    start_date = datetime(2020, 1, 1)
    end_date = start_date + timedelta(days=100)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Create price data with a simple pattern
    np.random.seed(42)  # For reproducibility
    price = 100.0
    prices = [price]
    
    for _ in range(1, len(dates)):
        change = np.random.normal(0, 1)  # Random price change
        price = max(price * (1 + change * 0.01), 0.1)  # Ensure price is positive
        prices.append(price)
    
    # Create OHLC data
    data = pd.DataFrame(index=dates)
    data['open'] = prices
    data['high'] = [p * (1 + np.random.uniform(0, 0.02)) for p in prices]  # High is up to 2% above open
    data['low'] = [p * (1 - np.random.uniform(0, 0.02)) for p in prices]   # Low is up to 2% below open
    data['close'] = [p * (1 + np.random.normal(0, 0.01)) for p in prices]  # Close is normally distributed around open
    data['volume'] = [int(np.random.uniform(1000, 10000)) for _ in prices]  # Random volume
    
    return data

def test_strategy_signals():
    # Create test data
    data = create_test_data()
    
    # Create strategy
    strategy = TestStrategy()
    
    # Generate signals
    signals = strategy.generate_signals(data)
    
    # Check signals
    assert 'signal' in signals.columns
    assert signals['signal'].isin([1.0, 0.0, -1.0]).all()
    assert len(signals) == len(data)

def test_portfolio():
    # Create test data
    data = create_test_data()
    
    # Create portfolio
    initial_capital = 100000.0
    portfolio = Portfolio(initial_capital)
    
    # Create a simple position
    portfolio.enter_position('AAPL', 10, data.iloc[10]['close'], data.index[10])
    
    # Check position
    assert len(portfolio.positions) == 1
    assert portfolio.positions[0].symbol == 'AAPL'
    assert portfolio.positions[0].quantity == 10
    assert portfolio.positions[0].entry_price == data.iloc[10]['close']
    
    # Exit position
    portfolio.exit_position(0, data.iloc[20]['close'], data.index[20])
    
    # Check position is closed
    assert len(portfolio.positions) == 0
    assert len(portfolio.closed_positions) == 1
    assert portfolio.closed_positions[0].exit_price == data.iloc[20]['close']
    
    # Check portfolio value
    profit = 10 * (data.iloc[20]['close'] - data.iloc[10]['close'])
    expected_value = initial_capital + profit
    assert portfolio.current_value == pytest.approx(expected_value)

def test_backtest():
    # Create test data
    data = create_test_data()
    
    # Create strategy
    strategy = TestStrategy()
    
    # Create backtest
    initial_capital = 100000.0
    backtest = Backtest(strategy, data, initial_capital)
    
    # Run backtest
    results = backtest.run()
    
    # Check results
    assert 'portfolio_value' in results.columns
    assert len(results) == len(data)
    assert results['portfolio_value'].iloc[0] == initial_capital
    
    # Check trades
    trades = backtest.get_trades()
    assert isinstance(trades, list)
    
    # Check performance metrics
    metrics = calculate_performance_metrics(results)
    assert 'total_return' in metrics
    assert 'sharpe_ratio' in metrics
    assert 'max_drawdown' in metrics

