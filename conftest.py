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

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    """Return a database session for testing."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    """Return a FastAPI test client with DB session override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db):
    """Create and return a test user."""
    user = User(
        email="test@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_strategy(db, test_user):
    """Create and return a test strategy."""
    strategy = Strategy(
        name="Test Strategy",
        description="A test strategy",
        type="moving_average",
        parameters={"short_window": 50, "long_window": 200},
        active=True,
        user_id=test_user.id,
    )
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy

@pytest.fixture
def auth_headers(test_user):
    """Return authorization headers for the test user."""
    access_token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {access_token}"}

