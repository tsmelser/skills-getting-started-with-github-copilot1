import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Initial activities data for resetting
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for intramural and inter-school competitions",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Volleyball Club": {
        "description": "Learn and play volleyball with fellow students",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["sarah@mergington.edu", "megan@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, drawing, and various art mediums",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["jasmine@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in plays and musicals throughout the school year",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["tyler@mergington.edu", "maya@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore advanced scientific concepts",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["lily@mergington.edu", "noah@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities dictionary to initial state before each test."""
    activities.clear()
    activities.update(initial_activities)

@pytest.fixture
def client():
    """Create a TestClient instance for the FastAPI app."""
    return TestClient(app, follow_redirects=False)

def test_get_activities(client):
    """Test GET /activities endpoint."""
    # Arrange
    # (client fixture provides the TestClient)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == activities

def test_signup_valid_activity(client):
    """Test POST /activities/{activity_name}/signup with a valid activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_participants = activities[activity_name]["participants"].copy()

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == len(initial_participants) + 1

def test_signup_invalid_activity(client):
    """Test POST /activities/{activity_name}/signup with an invalid activity."""
    # Arrange
    activity_name = "Invalid Activity"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_root_redirect(client):
    """Test GET / root endpoint redirects to static/index.html."""
    # Arrange
    # (client fixture provides the TestClient)

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"