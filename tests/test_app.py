"""Backend tests for the Mergington High School API."""

import pytest
from src.app import activities


class TestRootEndpoint:
    def test_root_redirects_to_static_index(self, client):
        # Arrange
        expected_location = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_location


class TestGetActivitiesEndpoint:
    def test_get_activities_returns_all_activities(self, client):
        # Arrange
        expected_names = {
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Volleyball Club",
            "Art Club",
            "Drama Club",
            "Debate Team",
            "Science Club",
        }

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert set(data.keys()) == expected_names

    def test_get_activities_contains_required_fields(self, client):
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        for activity_data in data.values():
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)


class TestSignupEndpoint:
    def test_signup_new_student(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_student_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Imaginary Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestRemoveParticipantEndpoint:
    def test_remove_existing_participant(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]

    def test_remove_nonexistent_participant_returns_404(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "nobody@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found in activity"

    def test_remove_from_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Unknown Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
