import os
import secrets
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import json
from peewee import *
from playhouse.shortcuts import model_to_dict
import libgravatar
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import *

from app.db import User, TimelinePost

load_dotenv()
app = Flask(__name__)

# flask-login initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"

# generate secret key
app.secret_key = secrets.token_urlsafe(16)

# store portfolio directory, then get json data path
portfolio_dir = os.path.dirname(os.path.realpath(__file__))
dataPath = os.path.join(portfolio_dir, "static/data.json")

data = open(dataPath)
data = json.load(data)


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
        "timeline.html",
        title="Sam Thibault - Timeline",
        url=os.getenv("URL"),
        name=current_user.name,
    )


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
##### END OF FRONTEND ROUTES #####


##### TIMELINE API ROUTES #####
# add a document by specifying field values in the request body
@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():

    # start by checking if the http request structure is correct
    req = request

    if "email" not in req.form:
        return "Invalid email, please try again", 400
    elif "content" not in req.form:
        return "Invalid content, please try again", 400

    # if it is, we can assign some variables
    name = current_user.name
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
        timeline_post = TimelinePost.create(
            name=name, email=email, content=content, avatar=avatar
        )
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


# delete a document by id
@app.route("/api/timeline_post", methods=["DELETE"])
def delete_time_line_post():

    # get the author name associated with the post id
    idToDelete = request.form["id"]
    try:
        qry = TimelinePost.get(idToDelete == TimelinePost.id)
    except:
        return "Invalid ID, please try again", 400

    postAuthor = qry.name

    # if the author matches the current user's name (case insensitive), try deleting, and return result message
    if postAuthor.lower() == current_user.name.lower() or current_user.name == "admin":
        qry = TimelinePost.delete().where(TimelinePost.id == idToDelete)
        qry.execute()
        return "deleted: " + idToDelete, 200
    else:
        return "You do not have permission to delete this post.", 400

##### END OF TIMELINE API ROUTES #####


##### AUTHENTICATION #####
# get user based on id
@login_manager.user_loader
def load_user(user_id):
    try:    
        return User.get(int(user_id))
    except:
        return None


# used to store new user in database
@app.route("/api/signup", methods=["POST"])
def post_signup():
    # ensure the request body contains the necessary information
    if "name" and "password" in request.form:
        name = request.form["name"]
        pw = request.form["password"]
        query = User.select().where(User.name == name)

        # username must be unique, if it already exists, return error
        if query.exists():
            return "User already exists!", 400

        # if name is valid, hash the password and create a user object
        hashed_pw = generate_password_hash(pw)

        user = User.create(name=name, password=hashed_pw)
        return model_to_dict(user)
    return "Something went wrong, please try again", 400


# used to validate a login attempt
@app.route("/api/signin", methods=["POST"])
def signin_check():
    if "name" and "password" in request.form:
        user = User.get_or_none(User.name == request.form["name"])

        # if the user exists, check to see if the password matches the stored hash value, if so: login to session
        if user != None:
            if check_password_hash(user.password, request.form["password"]) == True:
                login_user(user)
                return model_to_dict(user)
            else:
                return "Wrong password, please try again", 400

    return "Wrong username or password, please try again", 400


# signout method which clears session cookies and returns to the home page
@app.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect("/")

##### END OF AUTHENTICATION #####