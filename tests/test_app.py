import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern tests

def test_get_activities():
    # Arrange: (nothing to arrange for GET)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    # Arrange
    activity = "Chess Club"
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup
    client.post(f"/activities/{activity}/unregister", params={"email": email})

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.post(f"/activities/{activity}/unregister", params={"email": email})

def test_unregister_from_activity():
    # Arrange
    activity = "Chess Club"
    email = "testuser3@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

def test_unregister_not_registered():
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
