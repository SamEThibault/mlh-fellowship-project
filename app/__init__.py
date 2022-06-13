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
        "index.html", title="Team Jungle Portfolio", url=os.getenv("URL"), data=data
    )


@app.route("/about")
def about():
    return render_template(
        "about.html", title="Team Jungle Portfolio", url=os.getenv("URL"), data=data
    )


@app.route("/experience")
def experience():
    return render_template(
        "experience.html",
        title="Team Jungle Portfolio",
        url=os.getenv("URL"),
        data=data,
    )


@app.route("/map")
def map():
    return render_template(
        "map.html", title="Team Jungle Portfolio", url=os.getenv("URL"), data=data
    )


@app.route("/folium_map")
def folium_map():

    start_coords = (43.653, -79.383)
    folium_map = folium.Map(location=start_coords, zoom_start=3, tiles="Stamen Terrain")

    for i in range(0, len(data["locations"])):
        folium.Marker(
            location=[data["locations"][i]["latitude"], data["locations"][i]["longitude"]],
            popup=data["locations"][i]["name"],
            icon=folium.Icon(color=data["locations"][i]["color"]),
        ).add_to(folium_map)

    ## fix mobile view
    folium_map.get_root().header.add_child(
        folium.Element(
            '<meta name="viewport" content="width=device-width,'
            ' initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />'
        )
    )

    image_file = "/static/img/legend.jpg"
    FloatImage(image_file, bottom=0, left=0).add_to(folium_map)

    folium_map.save("templates/map.html")
    return render_template("mapindex.html")
