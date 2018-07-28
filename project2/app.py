import pandas as pd
import numpy as np
import os
import pymongo
import json
import flask
import geojson
import random
from flask import Flask, render_template
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson import json_util
from bson.json_util import dumps
from geojson import Feature, FeatureCollection, Point

uri_key = os.environ.get("uri")
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'earthquake'
app.config['MONGO_URI'] = uri_key

mongo = PyMongo(app)


@app.route('/')
def main():
    return render_template("landingpage.html")

app.route('/heatmap', method=["GET"])
def heatmap():
    return render_template("heatmap_2.html")

app.route('/tableau')
def tableau():
    return render_template("dashboard.html")

app.route('/d3')
def d3():
    return render_template("scatterplot.html")

@app.route("/earthquakedata")
def earthquakedata():
    connection = pymongo.MongoClient(uri_key)
    collection = connection["earthquake"]["all_records"]
    projects = collection.find({},{"_id":False}).limit(25000)
    # json_projects = []
    data = {
        "type": "FeatureCollection",
        "features": [
        {
            "type": "Feature",

            "properties" : {"mag":[d["mag"]], "place":[d["place"]], "time":[d["time"]]},

            "geometry" : {
                "type": "Point",
                "coordinates": [d["longitude"], d["latitude"],d["depth"]],
                },
        } for d in projects]
    }
    # json_projects.append(data)
    return jsonify(data)

@app.route("/geojson")
def geojsonSample():
    connection = pymongo.MongoClient(uri_key)
    collection = connection["earthquake"]["all_records"]
    projects = collection.find({},{"_id":False}).limit(2)
    sample = []
    sampleData = {
        "type": "FeatureCollection",
        "features": [
        {
            "type": "Feature",

            "properties" : {"mag":[d["mag"]], "place":[d["place"]], "time":[d["time"]]},

            "geometry" : {
                "type": "Point",
                "coordinates": [d["longitude"], d["latitude"],d["depth"]],
                },
        } for d in projects]
    }
    sample.append(sampleData)
    return jsonify(sample)

if __name__ == "__main__":
    app.run()



