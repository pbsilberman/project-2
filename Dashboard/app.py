import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/divvy.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/age")
def ridevol():
    query = "select cast(from_station_id as varchar) as from_station_id\
        , cast(t.tripduration as varchar) as tripduration\
        , cast(t.birthyear as varchar) as birthyear\
        , t.usertype\
        , cast(count(t.trip_id) as varchar) as trip_count\
        from trip as t\
        where t.birthyear != 'None'\
        group by t.birthyear"
        
    age_df = pd.read_sql_query(query,db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(age_df.to_dict(orient="records"))

@app.route("/rides")
def rideData():

    query = "select cast(from_station_id as varchar) as from_station_id\
        , cast(t.trip_id as varchar) as trip_id\
        , cast(t.to_station_id as varchar) as to_station_id\
        , cast(t.tripduration as varchar) as tripduration\
        , cast(t.birthyear as varchar) as birthyear\
        , cast(t.gender as varchar) as gender\
        , t.usertype\
        , cast (s.name as varchar) as from_station_id\
        , cast (s1.name as varchar) as to_station_id\
        from trip as t\
        join station as s on s.station_id = t.from_station_id\
        join station as s1 on s1.station_id = t.to_station_id\
        where t.birthyear != 'None'"
      
    rideData = pd.read_sql_query(query,db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(rideData.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)