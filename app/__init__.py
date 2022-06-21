import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import folium
import json
from folium.plugins import FloatImage

load_dotenv()
app = Flask(__name__)
data = open("static/data.json")
data = json.load(data)


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
