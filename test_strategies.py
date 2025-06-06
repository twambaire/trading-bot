import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.security import create_access_token
from app.db.models.user import User
from app.db.models.strategy import Strategy

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def create_test_user(db):
    user = User(
        email="test@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_test_strategy(db, user_id):
    strategy = Strategy(
        name="Test Strategy",
        description="A test strategy",
        type="moving_average",
        parameters={"short_window": 50, "long_window": 200},
        active=True,
        user_id=user_id,
    )
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy

def get_auth_header(user_id):
    access_token = create_access_token(data={"sub": str(user_id)})
    return {"Authorization": f"Bearer {access_token}"}

def test_create_strategy():
    # Create a test user
    db = TestingSessionLocal()
    user = create_test_user(db)
    db.close()
    
    # Test create strategy
    strategy_data = {
        "name": "New Strategy",
        "description": "A new test strategy",
        "type": "rsi",
        "parameters": {"window": 14, "oversold": 30, "overbought": 70},
        "active": True,
    }
    
    response = client.post(
        "/api/strategies",
        json=strategy_data,
        headers=get_auth_header(user.id),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == strategy_data["name"]
    assert data["description"] == strategy_data["description"]
    assert data["type"] == strategy_data["type"]
    assert data["parameters"] == strategy_data["parameters"]
    assert data["active"] == strategy_data["active"]
    assert "id" in data
    assert data["user_id"] == user.id

def test_get_strategies():
    # Create a test user and strategy
    db = TestingSessionLocal()
    user = create_test_user(db)
    strategy = create_test_strategy(db, user.id)
    db.close()
    
    # Test get strategies
    response = client.get(
        "/api/strategies",
        headers=get_auth_header(user.id),
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == strategy.name
    assert data[0]["id"] == strategy.id

def test_get_strategy():
    # Create a test user and strategy
    db = TestingSessionLocal()
    user = create_test_user(db)
    strategy = create_test_strategy(db, user.id)
    db.close()
    
    # Test get strategy
    response = client.get(
        f"/api/strategies/{strategy.id}",
        headers=get_auth_header(user.id),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == strategy.name
    assert data["id"] == strategy.id

def test_update_strategy():
    # Create a test user and strategy
    db = TestingSessionLocal()
    user = create_test_user(db)
    strategy = create_test_strategy(db, user.id)
    db.close()
    
    # Test update strategy
    update_data = {
        "name": "Updated Strategy",
        "description": "An updated test strategy",
        "active": False,
    }
    
    response = client.patch(
        f"/api/strategies/{strategy.id}",
        json=update_data,
        headers=get_auth_header(user.id),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["active"] == update_data["active"]
    assert data["type"] == strategy.type  # Unchanged
    assert data["parameters"] == strategy.parameters  # Unchanged

def test_delete_strategy():
    # Create a test user and strategy
    db = TestingSessionLocal()
    user = create_test_user(db)
    strategy = create_test_strategy(db, user.id)
    db.close()
    
    # Test delete strategy
    response = client.delete(
        f"/api/strategies/{strategy.id}",
        headers=get_auth_header(user.id),
    )
    assert response.status_code == 204
    
    # Verify strategy is deleted
    response = client.get(
        f"/api/strategies/{strategy.id}",
        headers=get_auth_header(user.id),
    )
    assert response.status_code == 404

