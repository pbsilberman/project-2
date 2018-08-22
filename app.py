import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import simplejson as json

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

# Save references to each table
stations = Base.classes.station
trips = Base.classes.trip


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/stationvolume")
def stationvollist():
    """Return a list of station locations and the number of trips per station."""
    query = "select cast(from_station_id as varchar) as from_station_id\
        , cast(s.latitude as varchar) as from_latitude\
        , cast(s.longitude as varchar) as from_longitude\
        , s.name\
        , cast(count(t.trip_id) as varchar) as trip_count\
        from station as s\
        join trip as t on s.station_id = t.from_station_id\
        group by from_station_id, s.latitude, s.longitude, s.name"

    trip_df = pd.read_sql_query(query,db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(trip_df.to_dict(orient="records"))


@app.route("/trips")
def triplist():
    """Return a list of trips by station."""
    # Use Pandas to perform the sql query
    query = "select cast(from_station_id as varchar) as from_station_id\
        , cast(s.latitude as varchar) as from_latitude\
        , cast(s.longitude as varchar) as from_longitude\
        , cast(to_station_id as varchar) as to_station_id\
        , cast(s1.latitude as varchar) as to_latitude\
        , cast(s1.longitude as varchar) as to_longitude\
        from trip as t\
        join station as s on s.station_id = t.from_station_id\
        join station as s1 on s1.station_id = t.to_station_id"

    trip_df = pd.read_sql_query(query,db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(trip_df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run()
