from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import datetime

from app.db.models.backtest import Backtest
from app.db.models.strategy import Strategy
from app.schemas.backtest import BacktestCreate
from app.backtester.data.fetcher import DataFetcher
from app.backtester.strategies.factory import StrategyFactory
from app.backtester.engine.backtest import Backtest as BacktestEngine

class BacktesterService:
    def run_backtest(
        self,
        db: Session,
        backtest_id: int,
    ) -> Dict:
        """
        Run a backtest.
        
        Args:
            db: The database session
            backtest_id: The backtest ID
            
        Returns:
            The backtest results
        """
        # Get backtest
        backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
        if not backtest:
            raise ValueError(f"Backtest not found: {backtest_id}")
        
        # Get strategy
        strategy = db.query(Strategy).filter(Strategy.id == backtest.strategy_id).first()
        if not strategy:
            raise ValueError(f"Strategy not found: {backtest.strategy_id}")
        
        # Update backtest status
        backtest.status = "running"
        db.commit()
        
        try:
            # Fetch data
            data_fetcher = DataFetcher()
            data = data_fetcher.fetch_data(
                backtest.symbol,
                backtest.start_date,
                backtest.end_date,
            )
            
            # Create strategy
            strategy_instance = StrategyFactory.create_strategy(
                strategy.type,
                {**strategy.parameters, **backtest.parameters},
            )
            
            # Run backtest
            backtest_engine = BacktestEngine(
                strategy=strategy_instance,
                data=data,
                initial_capital=backtest.initial_capital,
                commission=backtest.commission,
                slippage=backtest.slippage,
            )
            
            results = backtest_engine.run()
            
            # Update backtest
            backtest.results = results
            backtest.status = "completed"
            db.commit()
            
            return results
        except Exception as e:
            # Update backtest status
            backtest.status = "failed"
            backtest.error = str(e)
            db.commit()
            
            raise

    def generate_report(
        self,
        db: Session,
        backtest_id: int,
    ) -> str:
        """
        Generate a backtest report.
        
        Args:
            db: The database session
            backtest_id: The backtest ID
            
        Returns:
            The backtest report as HTML
        """
        # Get backtest
        backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
        if not backtest:
            raise ValueError(f"Backtest not found: {backtest_id}")
        
        if not backtest.results:
            raise ValueError(f"Backtest results not found: {backtest_id}")
        
        # Generate report
        from app.backtester.visualization.reports import create_performance_report
        report = create_performance_report(backtest.results)
        
        return report

backtester_service = BacktesterService()

