import copy

from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


def setup_function():
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


def test_get_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_success():
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate():
    email = activities["Chess Club"]["participants"][0]
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_missing_activity():
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "x@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success():
    email = activities["Chess Club"]["participants"][0]
    response = client.delete("/activities/Chess%20Club/unregister", params={"email": email})

    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_not_signed_up():
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": "not-signed@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_missing_activity():
    response = client.delete(
        "/activities/Unknown%20Club/unregister",
        params={"email": "x@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
