from app import app

def test_get():
    client = app.test_client()
    response = client.get("/api/data")
    assert response.status_code == 200
