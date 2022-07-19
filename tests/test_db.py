# Unit test for the MySQL database

import unittest
from peewee import *
from app.db import TimelinePost
from playhouse.shortcuts import model_to_dict


MODELS = [TimelinePost]

# instantiate a in-memory db for testing purposes
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):

    # create the db structure
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    # at the end, drop tables (to ensure data deletion) and close the database
    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()
    
    # send 2 POST queries, ensure id generates successfully
    def test_timeline_post(self):
        first_post = TimelinePost.create(email='john@example.com', content='Hello world I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(email='jane@example.com', content='Hello world I\'m Jane!')
        assert second_post.id == 2

        # test GET endpoint by fetching both queries, then assert that the responses match the POST queries
        response1 = model_to_dict(TimelinePost.get_by_id(1))
        response2 = model_to_dict(TimelinePost.get_by_id(2))

        assert first_post.email == response1["email"]
        assert first_post.content == response1["content"]
        assert first_post.created_at == response1["created_at"]
        
        assert second_post.email == response2["email"]
        assert second_post.content == response2["content"]
        assert second_post.created_at == response2["created_at"]