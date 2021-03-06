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
from app.oauth2 import create_access_token
from app import models


# Testing db config

# SQLALCHEMY_DATABASE_URL = 'postgresql:://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)

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


@pytest.fixture
def test_user(client):
    user_data = {"email": "mmk@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "mmk123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {token}'
    }
    
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    post_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"]
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user["id"]
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user["id"]
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user2["id"]
        },
    ]

    def create_post(post):
        return models.Post(**post)
    
    post_map = map(create_post, post_data)
    
    posts = list(post_map)
    
    session.add_all(posts)
    
    session.commit()
    
    return session.query(models.Post).all()




