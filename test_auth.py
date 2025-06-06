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

def test_login():
    # Create a test user
    db = TestingSessionLocal()
    user = create_test_user(db)
    db.close()
    
    # Test login
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_incorrect_password():
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "wrong_password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_inactive_user():
    # Create an inactive user
    db = TestingSessionLocal()
    user = User(
        email="inactive@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        is_active=False,
    )
    db.add(user)
    db.commit()
    db.close()
    
    # Test login with inactive user
    response = client.post(
        "/api/auth/login",
        data={"username": "inactive@example.com", "password": "password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Inactive user"

def test_get_current_user():
    # Create a test user
    db = TestingSessionLocal()
    user = create_test_user(db)
    db.close()
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # Test get current user
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "id" in response.json()

def test_get_current_user_invalid_token():
    response = client.get(
        "/api/users/me",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

