from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base

class TradingAccount(Base):
    __tablename__ = "trading_accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    broker = Column(String)
    account_id = Column(String)
    api_key = Column(String)
    api_secret = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="trading_accounts")
    orders = relationship("Order", back_populates="trading_account")
    positions = relationship("Position", back_populates="trading_account")

