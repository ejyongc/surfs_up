# Setup the Flack Weather App
## Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd

## Add SQLAlquemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setup Database
## Access the SQLite Database
engine = create_engine("sqlite:///hawaii.sqlite")
## Reflect the database into our classes.
Base = automap_base()
## Reflect the Database
Base.prepare(engine, reflect=True)
## Save our references to each table. create a variable for each of the classes so that we can reference them later.
Measurement = Base.classes.measurement
Station = Base.classes.station
## Finally, create a session link from Python to our database.
session = Session(engine)

# Setup Flask
app = Flask(__name__)
# define the welcome route
@app.route("/")

# Create Routes
# First, create a function welcome() with a return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# 9.5.3 Create precipitattion route.
@app.route("/api/v1.0/precipitation")
# create the precipitation () function. 
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip) 

# 9.5.4 Create stations route.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    # start by unraveling our results into a one-dimensional array
    stations = list(np.ravel(results))
    # jsonify the list and return it as JSON
    return jsonify(stations=stations)

# 9.5.5 Create monthly temperature route.
# defining the route
@app.route("/api/v1.0/tobs")
# create a function called temp_monthly()
def temp_monthly():
    # calculate the date one year ago from the last date in the database.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observation from the previous year. 
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # unravel the results into a one-dimensional array and convert that array into a list. Then jsonify the list and return our results.
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# 9.5.6 Statistics route.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Create a function called stats().
def stats(start=None, end=None):
# create a query to select min,max, and average temps from the SQL database. put it on a list
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # Query our database using the list that we just made. Then, we'll unravel the results into a one-dimensional array and convert them to a list. Finally, we will jsonify our results and return them.
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    # Calculate the temperature minimum, average, and maximum with the start and end dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)