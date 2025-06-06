import pandas as pd
from typing import Dict, Optional
import jinja2
import os
from datetime import datetime

def create_performance_report(results: Dict) -> str:
    """
    Create a performance report.
    
    Args:
        results: The backtest results
        
    Returns:
        An HTML report
    """
    # Extract data
    equity_curve = pd.DataFrame(results["equity_curve"])
    trades = pd.DataFrame(results["trades"])
    metrics = results["metrics"]
    
    # Create Jinja2 environment
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "templates")
    os.makedirs(template_dir, exist_ok=True)
    
    # Create template file if it doesn't exist
    template_path = os.path.join(template_dir, "performance_report.html")
    if not os.path.exists(template_path):
        with open(template_path, "w") as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Backtest Performance Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1, h2, h3 {
            color: #333;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .metrics {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 20px;
        }
        .metric-card {
            background-color: #f5f5f5;
            border-radius: 5px;
            padding: 15px;
            flex: 1;
            min-width: 200px;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            margin-top: 10px;
        }
        .chart {
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Backtest Performance Report</h1>
        <p>Generated on: {{ generated_date }}</p>
        
        <h2>Performance Metrics</h2>
        <div class="metrics">
            <div class="metric-card">
                <h3>Total Return</h3>
                <div class="metric-value">{{ '{:.2%}'.format(metrics.total_return) }}</div>
            </div>
            <div class="metric-card">
                <h3>Annual Return</h3>
                <div class="metric-value">{{ '{:.2%}'.format(metrics.annual_return) }}</div>
            </div>
            <div class="metric-card">
                <h3>Sharpe Ratio</h3>
                <div class="metric-value">{{ '{:.2f}'.format(metrics.sharpe_ratio) }}</div>
            </div>
            <div class="metric-card">
                <h3>Max Drawdown</h3>
                <div class="metric-value">{{ '{:.2%}'.format(metrics.max_drawdown) }}</div>
            </div>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <h3>Win Rate</h3>
                <div class="metric-value">{{ '{:.2%}'.format(metrics.win_rate) }}</div>
            </div>
            <div class="metric-card">
                <h3>Profit Factor</h3>
                <div class="metric-value">{{ '{:.2f}'.format(metrics.profit_factor) }}</div>
            </div>
            <div class="metric-card">
                <h3>Volatility</h3>
                <div class="metric-value">{{ '{:.2%}'.format(metrics.volatility) }}</div>
            </div>
        </div>
        
        <h2>Equity Curve</h2>
        <div class="chart">
            <img src="data:image/png;base64,{{ equity_curve_chart }}" alt="Equity Curve" style="width: 100%;">
        </div>
        
        <h2>Drawdown</h2>
        <div class="chart">
            <img src="data:image/png;base64,{{ drawdown_chart }}" alt="Drawdown" style="width: 100%;">
        </div>
        
        <h2>Returns Distribution</h2>
        <div class="chart">
            <img src="data:image/png;base64,{{ returns_distribution_chart }}" alt="Returns Distribution" style="width: 100%;">
        </div>
        
        <h2>Trades</h2>
        <div class="chart">
            <img src="data:image/png;base64,{{ trades_chart }}" alt="Trades" style="width: 100%;">
        </div>
        
        <h2>Trade List</h2>
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Symbol</th>
                    <th>Action</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Commission</th>
                </tr>
            </thead>
            <tbody>
                {% for trade in trades %}
                <tr>
                    <td>{{ trade.date }}</td>
                    <td>{{ trade.symbol }}</td>
                    <td>{{ trade.action }}</td>
                    <td>{{ trade.quantity }}</td>
                    <td>{{ '${:.2f}'.format(trade.price) }}</td>
                    <td>{{ '${:.2f}'.format(trade.commission) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>""")
    
    # Create Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=jinja2.select_autoescape(["html", "xml"])
    )
    
    # Load template
    template = env.get_template("performance_report.html")
    
    # Generate charts
    from app.backtester.visualization.charts import (
        create_equity_curve_chart,
        create_drawdown_chart,
        create_returns_distribution_chart,
        create_trades_chart,
    )
    
    equity_curve_chart = create_equity_curve_chart(equity_curve)
    drawdown_chart = create_drawdown_chart(equity_curve)
    returns_distribution_chart = create_returns_distribution_chart(equity_curve)
    
    # Only create trades chart if we have market data
    trades_chart = ""
    
    # Render template
    html = template.render(
        generated_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        metrics=metrics,
        equity_curve_chart=equity_curve_chart,
        drawdown_chart=drawdown_chart,
        returns_distribution_chart=returns_distribution_chart,
        trades_chart=trades_chart,
        trades=trades.to_dict(orient="records"),
    )
    
    return html

