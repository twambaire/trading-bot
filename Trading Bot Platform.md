# Trading Bot Platform

A full-stack trading bot platform with a React frontend, FastAPI backend, and backtester functionality.

## Features

- **User Authentication**: Secure login and registration system
- **Strategy Management**: Create, edit, and manage trading strategies
- **Backtesting Engine**: Test strategies against historical data
- **Live Trading**: Connect to brokers and execute trades
- **Performance Analytics**: Track and analyze trading performance
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation and settings management
- **JWT**: Authentication with JSON Web Tokens
- **PostgreSQL**: Relational database
- **Pandas & NumPy**: Data analysis and manipulation

### Frontend
- **React**: JavaScript library for building user interfaces
- **React Router**: Navigation and routing
- **Shadcn/UI**: UI component library
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Charting library for data visualization

## Project Structure

```
trading-bot/
├── backend/                 # FastAPI backend
│   ├── app/                 # Application code
│   │   ├── api/             # API endpoints
│   │   ├── backtester/      # Backtesting engine
│   │   ├── core/            # Core functionality
│   │   ├── db/              # Database models and session
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   ├── tests/               # Unit and integration tests
│   └── requirements.txt     # Python dependencies
├── trading-bot-frontend/    # React frontend
│   ├── public/              # Static files
│   ├── src/                 # Source code
│   │   ├── components/      # React components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── lib/             # Utility functions
│   │   └── pages/           # Page components
│   └── package.json         # Node.js dependencies
├── docker-compose.yml       # Docker Compose configuration
├── .env.example             # Example environment variables
├── DEPLOYMENT.md            # Deployment guide
└── README.md                # This file
```

## Getting Started

### Prerequisites

- Docker and Docker Compose (for containerized setup)
- Node.js 16+ and npm (for local frontend development)
- Python 3.9+ (for local backend development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/trading-bot.git
   cd trading-bot
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd trading-bot-frontend
npm install
npm run dev
```

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd trading-bot-frontend
npm test
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Shadcn/UI](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Pandas](https://pandas.pydata.org/)

