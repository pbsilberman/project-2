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


@app.route("/trip")
def trip():
    
    # Use Pandas to perform the sql query
    query = "select * from trip"
    trip=pd.read_sql_query(query,db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(trip.to_dict(orient="records"))

@app.route("/station")
def station():
    
    # Use Pandas to perform the sql query
    query = "select * from station"
    station=pd.read_sql_query(query,db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(station.to_dict(orient="records"))

    

if __name__ == "__main__":
    app.run(debug=True)