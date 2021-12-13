# Step 2:  Climate App

# import flask
from flask import Flask, jsonify

# additonal imports
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
from sqlalchemy import inspect


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create local app
app = Flask(__name__)

# define index route: Home page
@app.route("/")
def home():
    print(" Server accessed the home route")
    return (
        "Welcome to the Climate App Home Page! <br/>"
        f"Avalilable Routes: <br/>"
        f"------------------------ <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )
# define precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    print("Server accessed the Precipitation route")

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precipData = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date).all()

    session.close()

    #Convert the query results to a dictionary using date as the key and prcp as the value.
    #Return the JSON representation of your dictionary.
    precipitation_List = []
    for date, prcp in precipData:
        precipDictionary = {}
        precipDictionary[date] = prcp
        precipitation_List.append(precipDictionary)

    return jsonify (precipitation_List)

    

# define stations route
@app.route('/api/v1.0/stations')
def stations():
    print("Server accessed the Stations route")

    # Create session (link) from Python to the DB
    session = Session(engine)

    #Return a JSON list of stations from the dataset.
    station_list = session.query(Station.station).\
    order_by(Station.station).all()
    
    session.close()

    # store results as a list
    stationList= list(np.ravel(station_list))
    
    return jsonify (stationList)


# define tobs route
@app.route('/api/v1.0/tobs')
def tobs():
    print("Server accessed the tobs route")

    # Create session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    activeStationTemps = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == active_stations[0][0]).filter(Measurement.date >= query_date).all()

    session.close()

    #Convert the query results to a dictionary
    activeStationTemp_list = dict(activeStationTemps)
    
    #Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(activeStationTemp_list)
    
# define start/ end routes




#define the main function
if __name__ == "__main__":
    app.run(debug=True)