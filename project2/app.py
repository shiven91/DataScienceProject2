import pandas as pd
import numpy as np
import os
import pymongo
import json
import flask
from flask import Flask, render_template
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson import json_util
from bson.json_util import dumps

uri_key = os.environ.get("uri")
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'earthquake'
app.config['MONGO_URI'] = uri_key

mongo = PyMongo(app)

@app.route('/')
def main():
    return render_template("landingpage.html")

@app.route("/dataVisualization/", methods=['POST'])
def dataVisualization():
    return render_template('index.html')

@app.route("/earthquakedata")
def earthquakedata():
    connection = pymongo.MongoClient(uri_key)
    collection = connection["earthquake"]["all_records"]
    projects = collection.find({},{"_id":False})
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

if __name__ == "__main__":
    app.run()



