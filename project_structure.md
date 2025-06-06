# Trading Bot Project Structure

## Overview

This document outlines the structure and architecture of the trading bot project, which consists of:

1. FastAPI Backend
2. React Frontend
3. Backtester Module

The project is designed to provide a complete trading bot solution with strategy development, backtesting, and live trading capabilities.

## Directory Structure

```
trading-bot/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── strategies.py
│   │   │   │   ├── backtests.py
│   │   │   │   └── trading.py
│   │   │   └── dependencies.py
│   │   ├── core/             # Core functionality
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── db/               # Database models and connections
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── models/
│   │   │       ├── user.py
│   │   │       ├── strategy.py
│   │   │       ├── backtest.py
│   │   │       └── trade.py
│   │   ├── schemas/          # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── strategy.py
│   │   │   ├── backtest.py
│   │   │   └── trade.py
│   │   ├── services/         # Business logic
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── strategy.py
│   │   │   ├── backtest.py
│   │   │   └── trading.py
│   │   └── main.py           # FastAPI application entry point
│   ├── backtester/           # Backtesting module
│   │   ├── data/             # Data handling
│   │   │   ├── fetcher.py
│   │   │   ├── processor.py
│   │   │   └── storage.py
│   │   ├── engine/           # Backtesting engine
│   │   │   ├── backtest.py
│   │   │   ├── portfolio.py
│   │   │   └── performance.py
│   │   ├── strategies/       # Trading strategies
│   │   │   ├── base.py
│   │   │   ├── moving_average.py
│   │   │   ├── rsi.py
│   │   │   └── custom.py
│   │   └── visualization/    # Results visualization
│   │       ├── charts.py
│   │       └── reports.py
│   ├── tests/                # Backend tests
│   │   ├── api/
│   │   ├── services/
│   │   └── backtester/
│   ├── alembic/              # Database migrations
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Backend Docker configuration
├── frontend/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── api/              # API client
│   │   │   ├── client.js
│   │   │   ├── auth.js
│   │   │   ├── strategies.js
│   │   │   ├── backtests.js
│   │   │   └── trading.js
│   │   ├── components/       # React components
│   │   │   ├── common/
│   │   │   │   ├── Header.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   └── ...
│   │   │   ├── auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   ├── Register.jsx
│   │   │   │   └── ...
│   │   │   ├── dashboard/
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── PerformanceChart.jsx
│   │   │   │   └── ...
│   │   │   ├── strategies/
│   │   │   │   ├── StrategyList.jsx
│   │   │   │   ├── StrategyForm.jsx
│   │   │   │   └── ...
│   │   │   ├── backtester/
│   │   │   │   ├── BacktestForm.jsx
│   │   │   │   ├── BacktestResults.jsx
│   │   │   │   └── ...
│   │   │   └── trading/
│   │   │       ├── TradingDashboard.jsx
│   │   │       ├── OrderForm.jsx
│   │   │       └── ...
│   │   ├── contexts/         # React contexts
│   │   │   ├── AuthContext.jsx
│   │   │   └── ...
│   │   ├── hooks/            # Custom hooks
│   │   │   ├── useAuth.js
│   │   │   ├── useApi.js
│   │   │   └── ...
│   │   ├── pages/            # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Strategies.jsx
│   │   │   ├── Backtester.jsx
│   │   │   ├── Trading.jsx
│   │   │   └── ...
│   │   ├── utils/            # Utility functions
│   │   │   ├── format.js
│   │   │   ├── validation.js
│   │   │   └── ...
│   │   ├── App.jsx           # Main React component
│   │   └── index.jsx         # React entry point
│   ├── package.json          # Node.js dependencies
│   └── Dockerfile            # Frontend Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── .env.example              # Example environment variables
├── README.md                 # Project documentation
└── LICENSE                   # Project license
```

## Component Architecture

### Backend Architecture

The backend is built with FastAPI and follows a layered architecture:

1. **API Layer**: Handles HTTP requests and responses
2. **Service Layer**: Contains business logic
3. **Data Access Layer**: Interacts with the database
4. **Domain Layer**: Defines the core domain models

#### Key Components:

- **FastAPI Application**: The main application that handles HTTP requests
- **Pydantic Models**: Define the data schemas for request and response validation
- **SQLAlchemy Models**: Define the database models
- **Services**: Implement the business logic
- **Backtester**: Implements the backtesting functionality

### Frontend Architecture

The frontend is built with React and follows a component-based architecture:

1. **Pages**: Top-level components that represent different pages
2. **Components**: Reusable UI components
3. **Contexts**: Manage global state
4. **Hooks**: Encapsulate reusable logic
5. **API Client**: Handles communication with the backend

#### Key Components:

- **React Application**: The main application that renders the UI
- **React Router**: Handles client-side routing
- **Context API**: Manages global state
- **API Client**: Communicates with the backend API
- **UI Components**: Reusable UI components

### Backtester Architecture

The backtester is a module within the backend that simulates trading strategies:

1. **Data Module**: Fetches and processes historical data
2. **Engine Module**: Runs the backtesting simulation
3. **Strategy Module**: Implements trading strategies
4. **Performance Module**: Calculates performance metrics
5. **Visualization Module**: Generates charts and reports

#### Key Components:

- **Data Fetcher**: Fetches historical data from various sources
- **Backtest Engine**: Simulates trading strategies on historical data
- **Strategy Implementations**: Different trading strategies
- **Performance Calculator**: Calculates performance metrics
- **Visualization Tools**: Generates charts and reports

## API Endpoints

### Authentication

- `POST /api/auth/login`: Authenticate user and return token
- `POST /api/auth/register`: Register a new user
- `POST /api/auth/refresh`: Refresh authentication token
- `POST /api/auth/logout`: Logout user

### Users

- `GET /api/users/me`: Get current user information
- `PUT /api/users/me`: Update current user information
- `GET /api/users/{user_id}`: Get user information by ID
- `PUT /api/users/{user_id}`: Update user information by ID
- `DELETE /api/users/{user_id}`: Delete user by ID

### Strategies

- `GET /api/strategies`: Get all strategies
- `POST /api/strategies`: Create a new strategy
- `GET /api/strategies/{strategy_id}`: Get strategy by ID
- `PUT /api/strategies/{strategy_id}`: Update strategy by ID
- `DELETE /api/strategies/{strategy_id}`: Delete strategy by ID

### Backtests

- `GET /api/backtests`: Get all backtests
- `POST /api/backtests`: Create a new backtest
- `GET /api/backtests/{backtest_id}`: Get backtest by ID
- `DELETE /api/backtests/{backtest_id}`: Delete backtest by ID
- `GET /api/backtests/{backtest_id}/results`: Get backtest results
- `GET /api/backtests/{backtest_id}/chart`: Get backtest chart data

### Trading

- `GET /api/trading/accounts`: Get all trading accounts
- `POST /api/trading/accounts`: Connect a new trading account
- `GET /api/trading/accounts/{account_id}`: Get trading account by ID
- `DELETE /api/trading/accounts/{account_id}`: Disconnect trading account
- `GET /api/trading/orders`: Get all orders
- `POST /api/trading/orders`: Create a new order
- `GET /api/trading/orders/{order_id}`: Get order by ID
- `DELETE /api/trading/orders/{order_id}`: Cancel order by ID
- `GET /api/trading/positions`: Get all positions
- `GET /api/trading/positions/{position_id}`: Get position by ID
- `DELETE /api/trading/positions/{position_id}`: Close position by ID

## Data Models

### User

```python
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    strategies = relationship("Strategy", back_populates="user")
    backtests = relationship("Backtest", back_populates="user")
    trading_accounts = relationship("TradingAccount", back_populates="user")
```

### Strategy

```python
class Strategy(Base):
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

### Backtest

```python
class Backtest(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    parameters = Column(JSON)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)
    results = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="backtests")
    strategy = relationship("Strategy", back_populates="backtests")
```

### TradingAccount

```python
class TradingAccount(Base):
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
```

### Order

```python
class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    trading_account_id = Column(Integer, ForeignKey("trading_accounts.id"))
    external_id = Column(String, nullable=True)
    symbol = Column(String)
    order_type = Column(String)
    side = Column(String)
    quantity = Column(Float)
    price = Column(Float, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    trading_account = relationship("TradingAccount", back_populates="orders")
```

### Position

```python
class Position(Base):
    id = Column(Integer, primary_key=True, index=True)
    trading_account_id = Column(Integer, ForeignKey("trading_accounts.id"))
    external_id = Column(String, nullable=True)
    symbol = Column(String)
    side = Column(String)
    quantity = Column(Float)
    entry_price = Column(Float)
    current_price = Column(Float)
    unrealized_pnl = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    trading_account = relationship("TradingAccount", back_populates="positions")
```

## Technology Stack

### Backend

- **FastAPI**: Web framework for building APIs
- **SQLAlchemy**: ORM for database interactions
- **Pydantic**: Data validation and settings management
- **Alembic**: Database migrations
- **PostgreSQL**: Database
- **JWT**: Authentication
- **Pandas**: Data analysis
- **NumPy**: Numerical computations
- **Matplotlib/Plotly**: Data visualization

### Frontend

- **React**: UI library
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **TradingView Lightweight Charts**: Interactive charts
- **Material-UI**: UI component library
- **React Query**: Data fetching and caching
- **React Hook Form**: Form handling
- **Yup**: Form validation

### DevOps

- **Docker**: Containerization
- **Docker Compose**: Multi-container Docker applications
- **GitHub Actions**: CI/CD
- **Nginx**: Web server and reverse proxy

## Development Workflow

1. **Setup Development Environment**:
   - Clone the repository
   - Install dependencies
   - Set up environment variables

2. **Backend Development**:
   - Implement API endpoints
   - Implement business logic
   - Implement database models
   - Implement backtester

3. **Frontend Development**:
   - Implement UI components
   - Implement API client
   - Implement state management
   - Implement routing

4. **Testing**:
   - Write unit tests
   - Write integration tests
   - Perform manual testing

5. **Deployment**:
   - Build Docker images
   - Deploy to production
   - Monitor performance

## Conclusion

This document outlines the structure and architecture of the trading bot project. It provides a comprehensive overview of the project's components, their interactions, and the technology stack used. This structure is designed to be modular, scalable, and maintainable, allowing for easy extension and modification as requirements evolve.

