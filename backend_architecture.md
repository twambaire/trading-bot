# Backend Architecture

## Overview

The backend of the trading bot is built with FastAPI, a modern, fast (high-performance) web framework for building APIs with Python. The architecture follows a layered approach with clear separation of concerns, making it modular, maintainable, and testable.

## Architecture Layers

### 1. API Layer

The API layer is responsible for handling HTTP requests and responses. It defines the API endpoints, validates request data, and returns appropriate responses.

**Key Components:**
- **FastAPI Application**: The main application that handles HTTP requests
- **Routers**: Group related endpoints together
- **Dependency Injection**: Provide dependencies to endpoints
- **Request Validation**: Validate incoming request data
- **Response Models**: Define the structure of API responses

### 2. Service Layer

The service layer contains the business logic of the application. It orchestrates the flow of data between the API layer and the data access layer.

**Key Components:**
- **Service Classes**: Implement business logic
- **Use Cases**: Implement specific use cases
- **Validation**: Validate business rules
- **Coordination**: Coordinate between different components

### 3. Data Access Layer

The data access layer is responsible for interacting with the database. It abstracts away the details of database operations.

**Key Components:**
- **Repositories**: Provide methods to access and manipulate data
- **Database Models**: Define the structure of database tables
- **Database Session**: Manage database connections
- **Transactions**: Manage database transactions

### 4. Domain Layer

The domain layer defines the core domain models and business rules. It is independent of the other layers and contains the essential business logic.

**Key Components:**
- **Domain Models**: Define the core domain entities
- **Value Objects**: Define immutable objects with equality based on their attributes
- **Domain Services**: Implement domain-specific logic
- **Domain Events**: Define events that occur in the domain

## Component Interactions

The following diagram illustrates how the different components interact with each other:

```
+----------------+      +----------------+      +----------------+
|                |      |                |      |                |
|  API Layer     |----->|  Service Layer |----->|  Data Access   |
|  (FastAPI)     |      |  (Business     |      |  Layer         |
|                |<-----|  Logic)        |<-----|  (SQLAlchemy)  |
+----------------+      +----------------+      +----------------+
                                |
                                |
                                v
                        +----------------+
                        |                |
                        |  Domain Layer  |
                        |  (Core Models) |
                        |                |
                        +----------------+
```

1. The API layer receives HTTP requests and validates the request data.
2. The API layer calls the appropriate service in the service layer.
3. The service layer implements the business logic and calls the repositories in the data access layer.
4. The data access layer interacts with the database and returns the results to the service layer.
5. The service layer processes the results and returns them to the API layer.
6. The API layer formats the response and returns it to the client.

## FastAPI Application Structure

### Main Application

The main application is defined in `main.py` and is responsible for setting up the FastAPI application, including middleware, exception handlers, and routers.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)
```

### API Routers

API routers are defined in the `api` directory and group related endpoints together. Each router is responsible for a specific resource or feature.

```python
# api/endpoints/strategies.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_current_user, get_db
from app.schemas.strategy import Strategy, StrategyCreate, StrategyUpdate
from app.services.strategy import strategy_service
from app.db.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Strategy])
def get_strategies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all strategies for the current user.
    """
    return strategy_service.get_strategies(db, current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=Strategy)
def create_strategy(
    strategy_in: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new strategy.
    """
    return strategy_service.create_strategy(db, strategy_in, current_user.id)

@router.get("/{strategy_id}", response_model=Strategy)
def get_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a strategy by ID.
    """
    strategy = strategy_service.get_strategy(db, strategy_id)
    if not strategy or strategy.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

@router.put("/{strategy_id}", response_model=Strategy)
def update_strategy(
    strategy_id: int,
    strategy_in: StrategyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a strategy.
    """
    strategy = strategy_service.get_strategy(db, strategy_id)
    if not strategy or strategy.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy_service.update_strategy(db, strategy, strategy_in)

@router.delete("/{strategy_id}", response_model=Strategy)
def delete_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a strategy.
    """
    strategy = strategy_service.get_strategy(db, strategy_id)
    if not strategy or strategy.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy_service.delete_strategy(db, strategy)
```

### Dependencies

Dependencies are defined in the `api/dependencies.py` file and provide common functionality to endpoints, such as database sessions and authentication.

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.services.user import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_db():
    """
    Get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Get the current user from the token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_service.get_user(db, user_id)
    if user is None:
        raise credentials_exception
    return user
```

## Service Layer

The service layer contains the business logic of the application. Each service is responsible for a specific domain entity or feature.

```python
# services/strategy.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.models.strategy import Strategy
from app.schemas.strategy import StrategyCreate, StrategyUpdate

class StrategyService:
    def get_strategies(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Strategy]:
        """
        Get all strategies for a user.
        """
        return db.query(Strategy).filter(Strategy.user_id == user_id).offset(skip).limit(limit).all()

    def get_strategy(self, db: Session, strategy_id: int) -> Optional[Strategy]:
        """
        Get a strategy by ID.
        """
        return db.query(Strategy).filter(Strategy.id == strategy_id).first()

    def create_strategy(
        self, db: Session, strategy_in: StrategyCreate, user_id: int
    ) -> Strategy:
        """
        Create a new strategy.
        """
        strategy = Strategy(
            name=strategy_in.name,
            description=strategy_in.description,
            code=strategy_in.code,
            parameters=strategy_in.parameters,
            user_id=user_id,
        )
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
        return strategy

    def update_strategy(
        self, db: Session, strategy: Strategy, strategy_in: StrategyUpdate
    ) -> Strategy:
        """
        Update a strategy.
        """
        for field, value in strategy_in.dict(exclude_unset=True).items():
            setattr(strategy, field, value)
        db.commit()
        db.refresh(strategy)
        return strategy

    def delete_strategy(self, db: Session, strategy: Strategy) -> Strategy:
        """
        Delete a strategy.
        """
        db.delete(strategy)
        db.commit()
        return strategy

strategy_service = StrategyService()
```

## Data Access Layer

The data access layer is responsible for interacting with the database. It defines the database models and provides methods to access and manipulate data.

```python
# db/models/strategy.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    code = Column(String)
    parameters = Column(JSON)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="strategies")
    backtests = relationship("Backtest", back_populates="strategy")
```

## Schemas

Schemas are defined using Pydantic and are used for request and response validation.

```python
# schemas/strategy.py
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class StrategyBase(BaseModel):
    name: str
    description: Optional[str] = None
    code: str
    parameters: Dict

class StrategyCreate(StrategyBase):
    pass

class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    parameters: Optional[Dict] = None

class Strategy(StrategyBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
```

## Backtester Module

The backtester module is a key component of the backend that simulates trading strategies on historical data. It is designed to be modular and extensible, allowing for easy addition of new strategies and data sources.

### Data Module

The data module is responsible for fetching and processing historical data.

```python
# backtester/data/fetcher.py
import pandas as pd
import yfinance as yf
from typing import List, Optional
from datetime import datetime

class DataFetcher:
    def fetch_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Fetch historical data for a symbol.
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
        """
        data = {}
        for symbol in symbols:
            data[symbol] = self.fetch_data(symbol, start_date, end_date, interval)
        return data

data_fetcher = DataFetcher()
```

### Engine Module

The engine module is responsible for running the backtesting simulation.

```python
# backtester/engine/backtest.py
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime

from app.backtester.strategies.base import Strategy
from app.backtester.engine.portfolio import Portfolio

class Backtest:
    def __init__(
        self,
        strategy: Strategy,
        data: pd.DataFrame,
        initial_capital: float = 10000.0,
        commission: float = 0.0,
    ):
        self.strategy = strategy
        self.data = data
        self.initial_capital = initial_capital
        self.commission = commission
        self.portfolio = Portfolio(initial_capital)
        self.results = None

    def run(self) -> Dict:
        """
        Run the backtest.
        """
        for i in range(len(self.data)):
            # Get the current data
            current_data = self.data.iloc[:i+1]
            
            # Generate signals
            signals = self.strategy.generate_signals(current_data)
            
            # Execute trades
            self.portfolio.update(current_data.iloc[-1], signals, self.commission)
        
        # Calculate performance metrics
        self.results = self.portfolio.get_performance()
        return self.results

    def get_results(self) -> Dict:
        """
        Get the backtest results.
        """
        if self.results is None:
            self.run()
        return self.results
```

### Strategy Module

The strategy module defines the interface for trading strategies and provides implementations of common strategies.

```python
# backtester/strategies/base.py
import pandas as pd
from typing import Dict
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate trading signals based on the data.
        """
        pass

# backtester/strategies/moving_average.py
import pandas as pd
from typing import Dict

from app.backtester.strategies.base import Strategy

class MovingAverageStrategy(Strategy):
    def __init__(self, short_window: int = 50, long_window: int = 200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate trading signals based on moving average crossover.
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
            signals["price"] = data["Close"].iloc[-1]
        elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] >= long_ma.iloc[-2]:
            signals["action"] = "sell"
            signals["price"] = data["Close"].iloc[-1]
        
        return signals
```

### Performance Module

The performance module calculates performance metrics for the backtest.

```python
# backtester/engine/performance.py
import pandas as pd
import numpy as np
from typing import Dict

def calculate_performance(equity_curve: pd.Series) -> Dict:
    """
    Calculate performance metrics from an equity curve.
    """
    # Calculate returns
    returns = equity_curve.pct_change().dropna()
    
    # Calculate metrics
    total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1
    annual_return = (1 + total_return) ** (252 / len(returns)) - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe_ratio = annual_return / volatility if volatility != 0 else 0
    
    # Calculate drawdown
    drawdown = 1 - equity_curve / equity_curve.cummax()
    max_drawdown = drawdown.max()
    
    # Calculate win rate
    win_rate = len(returns[returns > 0]) / len(returns)
    
    return {
        "total_return": total_return,
        "annual_return": annual_return,
        "volatility": volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
    }
```

## Authentication and Security

The backend implements JWT-based authentication for secure API access.

```python
# core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: int, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password.
    """
    return pwd_context.hash(password)
```

## Configuration

The application configuration is managed using Pydantic's `BaseSettings` class, which allows for environment variable overrides.

```python
# core/config.py
from pydantic import BaseSettings, PostgresDsn
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Trading Bot"
    PROJECT_DESCRIPTION: str = "A trading bot with backtesting capabilities"
    PROJECT_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
            scheme="postgresql",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            path=f"/{self.POSTGRES_DB}",
        )

settings = Settings()
```

## Database

The database connection is managed using SQLAlchemy's `sessionmaker` and `create_engine` functions.

```python
# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

## Conclusion

The backend architecture is designed to be modular, maintainable, and testable. It follows a layered approach with clear separation of concerns, making it easy to extend and modify as requirements evolve. The FastAPI framework provides a solid foundation for building high-performance APIs, while SQLAlchemy and Pydantic provide robust data access and validation capabilities.

