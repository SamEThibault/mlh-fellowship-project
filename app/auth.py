from flask import Blueprint, request
from flask_login import login_user
from app.db import User
from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict

##### AUTHENTICATION #####

authentication_api = Blueprint('authentication_api', __name__)

# used to store new user in database
@authentication_api.route("/api/signup", methods=["POST"])
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
        User.create(name=name, password=hashed_pw)

        return "signup successful", 200
    return "Something went wrong, please try again", 400


# used to validate a login attempt
@authentication_api.route("/api/signin", methods=["POST"])
def signin_check():
    if "name" and "password" in request.form:
        user = User.get_or_none(User.name == request.form["name"])

        # if the user exists, check to see if the password matches the stored hash value, if so: login to session
        if user != None:
            if check_password_hash(user.password, request.form["password"]):
                login_user(user)
                return "login successful", 200
            else:
                return "Wrong password, please try again", 400

    return "Wrong username or password, please try again", 400

##### END OF AUTHENTICATION #####