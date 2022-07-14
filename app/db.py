import os
from peewee import *
import datetime
from flask_login import UserMixin

# if env variable TESTING is set to true, instantiate a in-memory db for testing purposes only
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    # for production, connect to real db specified by .env variables
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )

print(mydb)

# peewee model for the timeline posts
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    avatar = CharField(default="Testing")

    class Meta:
        database = mydb


# peewee model for the users
class User(UserMixin, Model):
    name = CharField(unique=True)
    password = CharField()


    class Meta:
        database = mydb

# connect to the database, and create tables using the above models
mydb.connect()
mydb.create_tables([TimelinePost, User])