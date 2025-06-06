from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Trading Account
class TradingAccountBase(BaseModel):
    name: str
    broker: str
    account_id: str
    api_key: str
    api_secret: str

class TradingAccountCreate(TradingAccountBase):
    pass

class TradingAccountUpdate(BaseModel):
    name: Optional[str] = None
    broker: Optional[str] = None
    account_id: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    is_active: Optional[bool] = None

class TradingAccountInDBBase(TradingAccountBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TradingAccount(TradingAccountInDBBase):
    pass

# Order
class OrderBase(BaseModel):
    symbol: str
    order_type: str
    side: str
    quantity: float
    price: Optional[float] = None

class OrderCreate(OrderBase):
    trading_account_id: int

class OrderUpdate(BaseModel):
    symbol: Optional[str] = None
    order_type: Optional[str] = None
    side: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    status: Optional[str] = None

class OrderInDBBase(OrderBase):
    id: int
    trading_account_id: int
    external_id: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Order(OrderInDBBase):
    pass

# Position
class PositionBase(BaseModel):
    symbol: str
    side: str
    quantity: float
    entry_price: float
    current_price: float
    unrealized_pnl: float

class PositionCreate(PositionBase):
    trading_account_id: int
    external_id: Optional[str] = None

class PositionUpdate(BaseModel):
    symbol: Optional[str] = None
    side: Optional[str] = None
    quantity: Optional[float] = None
    entry_price: Optional[float] = None
    current_price: Optional[float] = None
    unrealized_pnl: Optional[float] = None

class PositionInDBBase(PositionBase):
    id: int
    trading_account_id: int
    external_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Position(PositionInDBBase):
    pass

