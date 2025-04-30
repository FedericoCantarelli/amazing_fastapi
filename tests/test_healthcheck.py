from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv

client = TestClient(app)
load_dotenv("../.env.development")


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"api": "ready", "sha": "local", "env": "local"}
