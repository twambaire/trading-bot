from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    trading_account_id = Column(Integer, ForeignKey("trading_accounts.id"))
    external_id = Column(String, nullable=True)
    symbol = Column(String)
    order_type = Column(String)  # "market", "limit", "stop"
    side = Column(String)  # "buy", "sell"
    quantity = Column(Float)
    price = Column(Float, nullable=True)
    status = Column(String)  # "pending", "filled", "cancelled", "rejected"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    trading_account = relationship("TradingAccount", back_populates="orders")

