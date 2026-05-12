from urllib.parse import quote


def test_root_redirect(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity(client):
    activity_name = "Chess Club"
    url = f"/activities/{quote(activity_name, safe='')}/signup"

    response = client.post(url, params={"email": "newstudent@mergington.edu"})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up newstudent@mergington.edu for {activity_name}"}

    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities[activity_name]["participants"]


def test_signup_invalid_email(client):
    activity_name = "Chess Club"
    url = f"/activities/{quote(activity_name, safe='')}/signup"

    response = client.post(url, params={"email": "bad-email"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"


def test_signup_duplicate_email(client):
    activity_name = "Chess Club"
    url = f"/activities/{quote(activity_name, safe='')}/signup"

    response = client.post(url, params={"email": "michael@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_activity_not_found(client):
    response = client.post("/activities/Unknown/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity(client):
    activity_name = "Chess Club"
    url = f"/activities/{quote(activity_name, safe='')}/unregister"

    response = client.delete(url, params={"email": "michael@mergington.edu"})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered michael@mergington.edu from {activity_name}"}

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities[activity_name]["participants"]


def test_unregister_invalid_email(client):
    activity_name = "Chess Club"
    url = f"/activities/{quote(activity_name, safe='')}/unregister"

    response = client.delete(url, params={"email": "bad-email"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"


def test_unregister_not_signed_up(client):
    activity_name = "Chess Club"
    url = f"/activities/{quote(activity_name, safe='')}/unregister"

    response = client.delete(url, params={"email": "notregistered@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_activity_not_found(client):
    response = client.delete("/activities/Unknown/unregister", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
