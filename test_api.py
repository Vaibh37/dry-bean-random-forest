from fastapi.testclient import TestClient
from app import app
from frontend import SAMPLE

client = TestClient(app)

def test_valid_prediction():
    response = client.post("/predict", json=SAMPLE)

    assert response.status_code == 200
    assert response.json()["Prediction"] == "SEKER"


def test_invalid_area():
    invalid_sample = SAMPLE.copy()
    invalid_sample["Area"] = -1

    response = client.post("/predict", json=invalid_sample)

    assert response.status_code == 422
