import unittest
from peewee import *
from app import TimelinePost
from playhouse.shortcuts import model_to_dict

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()
    
    def test_timeline_post(self):
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world I\'m Jane!')
        assert second_post.id == 2

        response1 = model_to_dict(TimelinePost.get_by_id(1))
        response2 = model_to_dict(TimelinePost.get_by_id(2))

        assert first_post.name == response1["name"]
        assert first_post.email == response1["email"]
        assert first_post.content == response1["content"]
        assert first_post.created_at == response1["created_at"]

        assert second_post.name == response2["name"]
        assert second_post.email == response2["email"]
        assert second_post.content == response2["content"]
        assert second_post.created_at == response2["created_at"]