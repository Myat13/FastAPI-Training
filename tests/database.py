from modulefinder import Module
import pytest

# fastapi import
from fastapi.testclient import TestClient

# sqlalchemy import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# local imports
from app.main import app
from app.config import settings
from app.database import get_db, Base


# Testing db config

# SQLALCHEMY_DATABASE_URL = 'postgresql:://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()
    

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)

# client = TestClient(app)
