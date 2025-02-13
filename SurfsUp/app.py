# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

# Create engine to connect to the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Initialize Flask app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home route - List available routes
@app.route("/")
def welcome():
    return (
        f"Available API Routes:<br/>"
        f"/api/v1.0/precipitation - Last 12 months of precipitation data<br/>"
        f"/api/v1.0/stations - List of weather observation stations<br/>"
        f"/api/v1.0/tobs - Temperature observations for the most active station (last 12 months)<br/>"
        f"/api/v1.0/<start> - Min, Avg, Max temperatures from a start date<br/>"
        f"/api/v1.0/<start>/<end> - Min, Avg, Max temperatures for a date range"
    )

# Precipitation Route - Return JSON with last 12 months of precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Find the most recent date
    latest_date = session.query(func.max(Measurement.date)).scalar()
    latest_date_dt = dt.datetime.strptime(latest_date, "%Y-%m-%d")
    one_year_ago = latest_date_dt - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= one_year_ago.strftime("%Y-%m-%d"))\
        .all()

    # Convert query results to dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)

# Stations Route - Return JSON list of all stations
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(Station.station).all()
    
    # Convert to list
    stations_list = [station[0] for station in results]
    
    return jsonify(stations_list)

# TOBS Route - Return JSON list of temperature observations for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    # Find the most active station
    most_active_station = session.query(Measurement.station)\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc())\
        .first()[0]

    # Find the most recent date
    latest_date = session.query(func.max(Measurement.date)).scalar()
    latest_date_dt = dt.datetime.strptime(latest_date, "%Y-%m-%d")
    one_year_ago = latest_date_dt - dt.timedelta(days=365)

    # Query last 12 months of temperature observations for the most active station
    temp_observations = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= one_year_ago.strftime("%Y-%m-%d"))\
        .all()

    # Convert results to list of dictionaries
    tobs_list = [{date: tobs} for date, tobs in temp_observations]

    return jsonify(tobs_list)

# Start Route - Return min, avg, and max temperatures from a start date
@app.route("/api/v1.0/<start>")
def temp_from_start(start):
    # Query temperature statistics from the given start date
    temp_stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()

    return jsonify({"TMIN": temp_stats[0][0], "TAVG": temp_stats[0][1], "TMAX": temp_stats[0][2]})

# Start/End Route - Return min, avg, and max temperatures for a given date range
@app.route("/api/v1.0/<start>/<end>")
def temp_range(start, end):
    # Query temperature statistics from the given start to end date
    temp_stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date.between(start, end)).all()

    return jsonify({"TMIN": temp_stats[0][0], "TAVG": temp_stats[0][1], "TMAX": temp_stats[0][2]})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)