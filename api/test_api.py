import os
os.chdir('api')
import pytest
import main
from fastapi.testclient import TestClient
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
client = TestClient(main.app)


def test_predict_pos():
    main.startup_event()
    response = client.post("/predict", json={"body": "this movie was great"})
    assert response.status_code == 200
    assert response.json() == {"prediction": "positive"}
    os.remove("logs/predictions.json")
    os.rmdir('logs')


def test_predict_neg():
    main.startup_event()
    response = client.post("/predict", json={"body": "this movie was absolutely the worst terrible bad"})
    assert response.status_code == 200
    assert response.json() == {"prediction": "negative"}
    os.remove("logs/predictions.json")
    os.rmdir('logs')

def test_predict_bad():
    main.startup_event()
    response = client.post("/predict", json={"na": "this movie was absolutely the worst terrible bad"})
    assert response.status_code != 200
    if os.path.exists("logs"):
        os.rmdir('logs')