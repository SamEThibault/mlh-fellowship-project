import unittest
import os

os.environ["TESTING"] = "true"

from app import app
from tests import test_db


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Sam Thibault - Portfolio</title>" in html
        assert '<h1>&nbsp<span class="txt-type blink" data-wait="1500"' in html
        assert '<h1 class="hidden">Welcome to&nbspmy portfolio!</h1>' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        test_db.TestTimelinePost.test_timeline_post(self)
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 2

        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'class="form-label"' in html
        assert '<script src="../static/scripts/callAPI.js"></script>' in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        #POST request with empty name
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "",
                "email": "john@example.com",
                "content": "Hello World, I am John",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with missing content
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an email",
                "content": "Hello World, I am John",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

        #POST request with missing email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "content": "Hello World, I am John",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

        #POST request with empty email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "",
                "content": "Hello World, I am John",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html