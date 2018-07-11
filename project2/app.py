import pandas as pd
import numpy as np
import os
import pymongo
import json
import flask
import geojson
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

@app.route("/dataVisualization")
def dataVisualization():
    return render_template('heatmap_2.html')

@app.route("/earthquakedata")
def earthquakedata():
    connection = pymongo.MongoClient(uri_key)
    collection = connection["earthquake"]["all_records"]
    projects = collection.find({},{"_id":False}).limit(25000)
    json_projects = []
    data = {
        "type": "FeatureCollection",
        "features": [
        {
            "type": "Feature",

            "properties" : {"mag":[d["mag"]], "place":[d["place"]]},

            "geometry" : {
                "type": "Point",
                "coordinates": [d["longitude"], d["latitude"]],
                },
        } for d in projects]
    }
    json_projects.append(data)
    return jsonify(data)

# @app.route("/selectdata")
# def earthquakedata():
#     connection = pymongo.MongoClient(uri_key)
#     collection = connection["earthquake"]["all_records"]
#     projects = collection.find({},{"_id":False}).limit(10000)

if __name__ == "__main__":
    app.run()



