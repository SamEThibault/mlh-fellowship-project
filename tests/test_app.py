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