from datetime import date, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app

@pytest.fixture()
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

def test_create_word_and_due(client):
    response = client.post("/words/", json={"word": "bonjour", "definition": "hello", "language": "French"})
    assert response.status_code == 201
    assert response.json()["word"] == "bonjour"
    due = client.get("/words/due/")
    assert due.status_code == 200
    assert len(due.json()) == 1
    assert due.json()[0]["is_due"] is True

def test_review_score_five_schedules_five_days(client):
    word = client.post("/words/", json={"word": "hola", "definition": "hello", "language": "Spanish"}).json()
    response = client.post(f"/words/{word['id']}/review/", json={"score": 5})
    assert response.status_code == 201
    data = response.json()
    assert data["interval"] == 5
    assert data["repetition"] == 1
    assert date.fromisoformat(data["next_review"][:10]) == date.today() + timedelta(days=5)
    assert client.get("/words/due/").json() == []

def test_low_score_resets_to_one_day(client):
    word = client.post("/words/", json={"word": "gracias", "definition": "thank you", "language": "Spanish"}).json()
    response = client.post(f"/words/{word['id']}/review/", json={"score": 1})
    assert response.status_code == 201
    data = response.json()
    assert data["interval"] == 1
    assert data["repetition"] == 0
    assert date.fromisoformat(data["next_review"][:10]) == date.today() + timedelta(days=1)

def test_invalid_score_and_missing_word(client):
    word = client.post("/words/", json={"word": "ciao", "definition": "hello", "language": "Italian"}).json()
    assert client.post(f"/words/{word['id']}/review/", json={"score": 6}).status_code == 422
    assert client.post("/words/999/review/", json={"score": 4}).status_code == 404

def test_history_and_delete(client):
    word = client.post("/words/", json={"word": "merci", "definition": "thank you", "language": "French"}).json()
    client.post(f"/words/{word['id']}/review/", json={"score": 4})
    history = client.get("/words/history/")
    assert history.status_code == 200
    assert history.json()["total_words"] == 1
    assert history.json()["total_reviews"] == 1
    assert client.delete(f"/words/{word['id']}").status_code == 204
    assert client.get("/words/due/").json() == []

def test_blank_word_rejected(client):
    response = client.post("/words/", json={"word": "  ", "definition": "hello", "language": "French"})
    assert response.status_code == 422
