# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
import base64
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///california2.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
California = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")

def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/EV_stations"
        f"/api/v1.0/city"
    )
# List of EV Stations by city
@app.route("/api/v1.0/EV_Stations")
def EV_Stations():
    #Create our session 9link) from Python to the DB:
    session = Session(engine)

    """List of all EV Stations"""
    results = session .query(California.station_name).all()

    session.close()

    #Convert to better list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

if __name__ == "__main__":
    app.run(debug=True)