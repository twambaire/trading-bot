# Trading Bot Deployment Guide

This guide provides instructions for deploying the Trading Bot application, which consists of a FastAPI backend, a React frontend, and a backtester module.

## Prerequisites

- Docker and Docker Compose
- Node.js 16+ and npm (for local development)
- Python 3.9+ (for local development)
- A server with at least 2GB RAM and 1 CPU core

## Directory Structure

```
trading-bot/
├── backend/             # FastAPI backend
├── trading-bot-frontend/ # React frontend
├── docker-compose.yml   # Docker Compose configuration
└── .env                 # Environment variables
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Backend settings
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://postgres:postgres@db:5432/tradingbot

# Frontend settings
VITE_API_URL=http://localhost:8000

# Database settings
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tradingbot
```

## Deployment Steps

### 1. Build and Deploy with Docker Compose

The easiest way to deploy the application is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/yourusername/trading-bot.git
cd trading-bot

# Create .env file (see above)
touch .env

# Build and start the containers
docker-compose up -d --build
```

This will start the following services:
- PostgreSQL database
- FastAPI backend on port 8000
- React frontend on port 3000
- Nginx reverse proxy on port 80

### 2. Manual Deployment

#### Backend Deployment

```bash
cd trading-bot/backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend Deployment

```bash
cd trading-bot/trading-bot-frontend

# Install dependencies
npm install

# Build for production
npm run build

# Serve the built files (example with serve)
npx serve -s dist
```

## Updating the Application

### Docker Compose Deployment

```bash
# Pull the latest changes
git pull

# Rebuild and restart the containers
docker-compose down
docker-compose up -d --build
```

### Manual Deployment

#### Backend Update

```bash
cd trading-bot/backend
source venv/bin/activate

# Pull the latest changes
git pull

# Update dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Restart the server
# (depends on your process manager)
```

#### Frontend Update

```bash
cd trading-bot/trading-bot-frontend

# Pull the latest changes
git pull

# Update dependencies
npm install

# Rebuild
npm run build
```

## Monitoring and Maintenance

### Logs

```bash
# Docker Compose logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Database Backup

```bash
# Backup PostgreSQL database
docker-compose exec db pg_dump -U postgres tradingbot > backup.sql

# Restore PostgreSQL database
cat backup.sql | docker-compose exec -T db psql -U postgres tradingbot
```

## Security Considerations

1. **API Security**:
   - The backend uses JWT authentication
   - Set a strong SECRET_KEY in the .env file
   - Consider using HTTPS in production

2. **Database Security**:
   - Use strong passwords for the database
   - Restrict database access to only the backend service
   - Regularly backup the database

3. **Environment Variables**:
   - Never commit .env files to version control
   - Use different secrets for development and production

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Check if the database container is running: `docker-compose ps`
   - Verify database credentials in the .env file
   - Check database logs: `docker-compose logs db`

2. **Backend API Issues**:
   - Check backend logs: `docker-compose logs backend`
   - Verify the API is accessible: `curl http://localhost:8000/api/health`
   - Check if the database migrations have been applied

3. **Frontend Issues**:
   - Check if the API URL is correctly set in the .env file
   - Verify the frontend is built correctly: `docker-compose exec frontend ls -la /app/dist`
   - Check browser console for JavaScript errors

## Production Recommendations

1. **Use a Production-Ready Web Server**:
   - Configure Nginx or Apache as a reverse proxy
   - Enable HTTPS with Let's Encrypt certificates

2. **Set Up Monitoring**:
   - Implement health checks for all services
   - Set up alerts for critical errors
   - Monitor system resources (CPU, memory, disk)

3. **Implement CI/CD**:
   - Automate testing and deployment
   - Use staging environments for testing before production

4. **Regular Backups**:
   - Schedule regular database backups
   - Store backups in a secure, off-site location

