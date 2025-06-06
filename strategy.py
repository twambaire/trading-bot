from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    type = Column(String)  # e.g., "moving_average", "rsi"
    code = Column(String)
    parameters = Column(JSON)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="strategies")
    backtests = relationship("Backtest", back_populates="strategy")

