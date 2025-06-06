from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    trading_account_id = Column(Integer, ForeignKey("trading_accounts.id"))
    external_id = Column(String, nullable=True)
    symbol = Column(String)
    side = Column(String)  # "long", "short"
    quantity = Column(Float)
    entry_price = Column(Float)
    current_price = Column(Float)
    unrealized_pnl = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    trading_account = relationship("TradingAccount", back_populates="positions")

