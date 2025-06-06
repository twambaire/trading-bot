# Trading Bot Backend

This is the backend for the Trading Bot application. It's built with FastAPI and provides a REST API for the frontend.

## Features

- User authentication and authorization
- Trading strategy management
- Backtesting
- Trading account management
- Order and position management

## Requirements

- Python 3.8+
- PostgreSQL

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
5. Create the database:
   ```bash
   # Using psql
   createdb tradingbot
   ```

## Running the Application

```bash
python run.py
```

The API will be available at http://localhost:8000.

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── api/                  # API endpoints
│   ├── endpoints/        # API endpoint modules
│   └── dependencies.py   # API dependencies
├── core/                 # Core modules
│   ├── config.py         # Configuration
│   └── security.py       # Security utilities
├── db/                   # Database
│   ├── models/           # Database models
│   ├── base.py           # Base model
│   └── session.py        # Database session
├── schemas/              # Pydantic schemas
├── services/             # Business logic
├── backtester/           # Backtesting module
│   ├── data/             # Data handling
│   ├── engine/           # Backtesting engine
│   ├── strategies/       # Trading strategies
│   └── visualization/    # Results visualization
└── main.py               # FastAPI application
```

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

```bash
# Initialize migrations
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

