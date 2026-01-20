from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_read_main():
    """API's main page (docs) is accessible?"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_health_check():
    """Prediction endpoint is returning 422 (Unprocessable Entity)?
    (Because we send no data, it should return 422, showing that the API is running)
    """
    response = client.post("/predict")
    assert response.status_code == 422