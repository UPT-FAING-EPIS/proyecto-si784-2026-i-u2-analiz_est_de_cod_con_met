from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # Asegura que devuelva un HTML o el archivo esperado
    assert "text/html" in response.headers.get("content-type", "")

def test_read_dashboard():
    response = client.get("/dashboard")
    assert response.status_code == 200

def test_read_admin():
    response = client.get("/admin")
    assert response.status_code == 200
