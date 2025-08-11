from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.__version__ import version
from app.main import app

client = TestClient(app)
load_dotenv("../.env.development")


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "api": "ready",
        "sha": "local",
        "env": "local",
        "version": version,
    }
