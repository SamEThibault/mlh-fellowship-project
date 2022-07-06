import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import werkzeug
import libgravatar

load_dotenv()
app = Flask(__name__)

# store portfolio directory, then get json data path
portfolio_dir = os.path.dirname(os.path.realpath(__file__))
dataPath = os.path.join(portfolio_dir, "static/data.json")

data = open(dataPath)
data = json.load(data)

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
        "index.html", title="Sam Thibault - Home", url=os.getenv("URL"), data=data
    )


@app.route("/about")
def about():
    return render_template(
        "about.html", title="Sam Thibault - About", url=os.getenv("URL"), data=data
    )


@app.route("/experience")
def experience():
    return render_template(
        "experience.html",
        title="Sam Thibault - Experience",
        url=os.getenv("URL"),
        data=data,
    )


@app.route("/timeline")
def timeline():
    return render_template(
        "timeline.html", title="Sam Thibault - Timeline", url=os.getenv("URL")
    )


##### API ROUTES #####
# add a document by specifying field values in the request body
@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():

    name = request.form["name"]
    print(name)
    email = request.form["email"]
    print(email)
    content = request.form["content"]
    print(content)

    # if the request body is formatted properly, and frontend form validation fails, ensure the fields are formatted properly
    if content == "":
        return "Invalid content, please try again", 400
    elif "@" not in email or "." not in email:
        return "Invalid email, please try again", 400
    elif name == "":
        return "Invalid name, please try again", 400
    else:
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
    idToDelete = request.form["id"]
    qry = TimelinePost.delete().where(TimelinePost.id == idToDelete)
    result = qry.execute()

    if result == 0:
        return "error, invalid ID. Try again", 400
    else:
        return "deleted: " + idToDelete


# this mapping deletes all documents from the database (used for testing)
@app.route("/api/timeline_post/purge", methods=["DELETE"])
def delete_all():
    qry = TimelinePost.delete()
    qry.execute()
    return "deleted all rows"


# receive email in body, and return Gravatage img link
@app.route("/api/get_gravatar", methods=["POST"])
def get_gravatar():
    email = request.form["email"]
    g = libgravatar.Gravatar(email).get_image(default="mm")
    print(g)
    return g


# for erronous request bodies, return the appropriate message depending on missing fields
@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    req = request
    if "name" not in req.form:
        return "Invalid name, please try again", 400
    elif "email" not in req.form:
        return "Invalid email, please try again", 400
    elif "content" not in req.form:
        return "Invalid content, please try again", 400
    else:
        return "Invalid format, please try again"
