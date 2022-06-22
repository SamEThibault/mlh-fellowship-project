import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
from flask_cors import CORS


load_dotenv()
app = Flask(__name__)
CORS(app)
data = open("static/data.json")
data = json.load(data)

# MySQL db variable using peewee and environment variables
mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)

# peewee model for the timeline posts
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


# connect to the database, and create a table using the above model
mydb.connect()
mydb.create_tables([TimelinePost])


##### FRONTEND ROUTES #####
# routes send the loaded json object "data" to display personal information
@app.route("/")
def index():
    return render_template(
        "index.html", title="Sam Thibault - Portfolio", url=os.getenv("URL"), data=data
    )


@app.route("/about")
def about():
    return render_template(
        "about.html", title="Sam Thibault - Portfolio", url=os.getenv("URL"), data=data
    )


@app.route("/experience")
def experience():
    return render_template(
        "experience.html",
        title="Sam Thibault - Portfolio",
        url=os.getenv("URL"),
        data=data,
    )

# on page load, GET all timeline posts and send through data Jinja variable to display
@app.route("/timeline")
def timeline():
    return render_template(
        "timeline.html", 
        title = "Sam Thibault - Portfolio",
        url=os.getenv("URL"),
        data=get_time_line_post()
    )

##### TIMELINE API ROUTES #####
# add a document by specifying field values in the request body
@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():

    name = request.form["name"]
    print(name)
    email = request.form["email"]
    print(email)
    content = request.form["content"]
    print(content)
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


# get all documents
@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


# delete a document by name
@app.route("/api/timeline_post", methods=["DELETE"])
def delete_time_line_post():
    nameToDelete = request.form["name"]
    qry = TimelinePost.delete().where(TimelinePost.name == nameToDelete)
    qry.execute()
    return "deleted: " + nameToDelete


# this mapping deletes all documents from the database (used for testing)
@app.route("/api/timeline_post/purge", methods=["DELETE"])
def delete_all():
    qry = TimelinePost.delete()
    qry.execute()
    return "deleted all rows"
