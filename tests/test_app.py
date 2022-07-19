# Integration test for major frontend pages and main API endpoints
import unittest
import os

# set env variable to ensure db set up is in-memory (in init)
os.environ["TESTING"] = "true"

from app import app
from tests import test_db


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    # home frontend test: ensure general elements are properly fetched
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<h1 class="hidden">Welcome to&nbspmy portfolio!</h1>' in html
        assert '<h1>&nbsp<span class="txt-type blink" data-wait="1500"' in html
        assert '<h1 class="hidden">Welcome to&nbspmy portfolio!</h1>' in html

    # Timeline API/frontend test
    # Note: not testing the name field since the API does not expect a name field in the request. It
    # is automatically added using the authenticated user's username. Unit tests are not included for the
    # authentication feature
    def test_timeline(self):

        # GET posts, should return empty list of timeline objs
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # POST 2 queries using the db test, then GET and ensure response contains 2 timeline objs
        test_db.TestTimelinePost.test_timeline_post(self)
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 2

    # send bad requests and test responses
    def test_malformed_timeline_post(self):

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": ""},
        )

        json = response.get_json()
        assert json["status"] == 400
        assert "Empty content" in json["body"]

        # POST request with missing content
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com"},
        )
        json = response.get_json()
        assert json["status"] == 400
        assert "Empty content" in json["body"]

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an email",
                "content": "Hello World, I am John",
            },
        )

        json = response.get_json()
        assert json["status"] == 400
        assert "Invalid email" in json["body"]

        # POST request with missing email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "content": "Hello World, I am John",
            },
        )

        json = response.get_json()
        assert json["status"] == 400
        assert "Invalid email" in json["body"]

        # POST request with empty email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "",
                "content": "Hello World, I am John",
            },
        )

        json = response.get_json()
        assert json["status"] == 400
        assert "Invalid email" in json["body"]
