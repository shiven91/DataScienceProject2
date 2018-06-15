import pandas as pd
import numpy as np
import os
import pymongo
import json
import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'earthquake'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/earthquake'

mongo = PyMongo(app)

data_file = os.path.join("data","all_month.csv")

all_month_pd = pd.read_csv(data_file)
all_month_pd['time'] = pd.to_datetime(all_month_pd['time'])
all_month_pd['Date'] = all_month_pd['time'].dt.strftime('%Y-%m-%d')
all_month_pd['Time'] = all_month_pd['time'].dt.strftime('%H:%M:%S')
cleaned_df = all_month_pd[["Date","Time","latitude","longitude","mag","type","place"]].copy()
cleaned_df["place"] = cleaned_df["place"].str.split("of").str[1]
cleaned_df.to_csv("cleanedNewData.csv")

def import_content(filepath):
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['earthquake']
    collection_name = 'all_month'
    db_cm = mng_db[collection_name]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json)

@app.route('/data')
def get_all_data():
    all_data = mongo.db.all_month
    output = []
    for s in all_data.find():
        output.append({'place' : s['place']})
    return jsonify({'result' : output})


if __name__ == "__main__":
    filepath = os.path.join("cleanedNewData.csv")
    import_content(filepath)
    app.run()



