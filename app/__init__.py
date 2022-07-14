import os
from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import json
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import werkzeug
import libgravatar
from flask_login import LoginManager, UserMixin, login_required, login_user

load_dotenv()
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"

app.secret_key = os.getenv("SECRET_KEY")

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
        port=3306
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
@login_required
def timeline():
    return render_template(
        "timeline.html", title="Sam Thibault - Timeline", url=os.getenv("URL")
    )


##### Authentication #####
# get user based on id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/signin", methods=["GET"])
def signin():
    return render_template(
        "signin.html", title="Sam Thibault - Sign in", url=os.getenv("URL")
    )

@app.route("/signup", methods=["GET"])
def get_signup():
    return render_template(
        "signup.html", title="Sam Thibault - Sign up", url=os.getenv("URL")
    )

# used to store new user in database
@app.route("/api/signup", methods=["POST"])
def post_signup():
    # ensure the request body contains the necessary information
    if "name" and "password" in request.form:
            name = request.form["name"]
            password = request.form["password"]
            query = User.select().where(User.name == name)

            # username must be unique, if it already exists, return error
            if query.exists():
                return "User already exists!", 400

            user = User.create(name=name, password=password)
            print(model_to_dict(user))
            return render_template(
                "signin.html", title="Sam Thibault - Sign in", url=os.getenv("URL")
            )
    return "Something went wrong, please try again", 400

# used to validate a login attempt
@app.route("/api/signin", methods=["GET"])
def signin_check():
    if "name" and "password" in request.form:
        user = User.get_or_none(User.name == request.form["name"])
        if user != None:
            if request.form["password"] == user.password:
                login_user(user)
                return render_template(
        "timeline.html", title="Sam Thibault - Timeline", url=os.getenv("URL")
    )
    else:
        return "Wrong username or password, please try again", 400

##### API ROUTES #####
# add a document by specifying field values in the request body
@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():

    # start by checking if the http request structure is correct
    req = request
    if "name" not in req.form:
        return "Invalid name, please try again", 400
    elif "email" not in req.form:
        return "Invalid email, please try again", 400
    elif "content" not in req.form:
        return "Invalid content, please try again", 400

    # if it is, we can assign some variables
    name = req.form["name"]
    print(name)
    email = req.form["email"]
    print(email)
    content = req.form["content"]
    print(content)

    # use libgravatar to find profile image link for the submitted email, default to basic avatar
    avatar = libgravatar.Gravatar(email).get_image(default="mm")

    # if the request body is formatted properly, and frontend form validation fails, ensure the fields are formatted properly here
    if content == "":
        return "Invalid content, please try again", 400
    elif "@" not in email or "." not in email:
        return "Invalid email, please try again", 400
    elif name == "":
        return "Invalid name, please try again", 400
    else:
        timeline_post = TimelinePost.create(name=name, email=email, content=content, avatar=avatar)
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