from flask import Blueprint, request, Response
from app.db import TimelinePost
from flask_login import current_user
from playhouse.shortcuts import model_to_dict
from peewee import *
import libgravatar

##### TIMELINE API ROUTES #####
# add a document by specifying field values in the request body

timeline_api = Blueprint('timeline_api', __name__)

@timeline_api.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():

    # start by checking if the http request structure is correct
    req = request

    if "email" not in req.form:
        return {"body" : "Empty email, please try again", "status" : 400}
    elif "content" not in req.form:
        return {"body" : "Empty content, please try again", "status" : 400}

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
        return {"body" : "Empty content, please try again", "status" : 400}
    elif "@" not in email or "." not in email:
        return {"body" : "Invalid email, please try again", "status" : 400}
    elif name == "":
        return {"body" : "Name error, please try again", "status" : 400}
    else:
        timeline_post = TimelinePost.create(
            name=name, email=email, content=content, avatar=avatar
        )
        return model_to_dict(timeline_post)


# get all documents
@timeline_api.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


# delete a document by id
@timeline_api.route("/api/timeline_post", methods=["DELETE"])
def delete_time_line_post():

    # get the author name associated with the post id
    idToDelete = request.form["id"]
    try:
        qry = TimelinePost.get(idToDelete == TimelinePost.id)
    except:
        return {"body" : "Invalid ID, please try again", "status" : 400}

    postAuthor = qry.name

    # if the author matches the current user's name (case insensitive), try deleting, and return result message
    if postAuthor.lower() == current_user.name.lower() or current_user.name == "admin":
        qry = TimelinePost.delete().where(TimelinePost.id == idToDelete)
        qry.execute()
        return "deleted: " + idToDelete, 200
    else:
        return {"body" : "You do not have permission to delete this post", "status" : 400}

##### END OF TIMELINE API ROUTES #####