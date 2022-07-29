import os
import secrets
from flask import Flask, render_template, redirect
from dotenv import load_dotenv
import json
from flask_login import LoginManager, login_required, current_user, logout_user

from app.timeline import timeline_api
from app.auth import authentication_api
from app.db import User

# load env variables, set app variable, and register blueprints to access all api routes
load_dotenv()
app = Flask(__name__)
app.register_blueprint(timeline_api)
app.register_blueprint(authentication_api)

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

# get user based on id
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(int(user_id))
    except:
        return None


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


# signout method which clears session cookies and returns to the home page
@app.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect("/")


##### END OF FRONTEND ROUTES #####
