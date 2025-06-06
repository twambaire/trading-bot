from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base

class Backtest(Base):
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String)
    parameters = Column(JSON)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    initial_capital = Column(Float, default=10000.0)
    commission = Column(Float, default=0.0)
    slippage = Column(Float, default=0.0)
    status = Column(String)  # "pending", "running", "completed", "failed"
    error = Column(String, nullable=True)
    results = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="backtests")
    strategy = relationship("Strategy", back_populates="backtests")

