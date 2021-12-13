# Step 2:  Climate App

# import flask
from flask import Flask, jsonify

# additonal imports
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
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
# Create our session (link) from Python to the DB
session = Session(engine)

# Create local app
app = Flask(__name__)

# define index route: Home page
@app.route("/")
def home():
    print(" Server accessed the home route")
    return (
        "Welcome to the Climate App Home Page! <br/>"
        "Avalilable Routes: <br/>"
        "------------------------ <br/>"
        "/api/v1.0/precipitation <br/>"
        "/api/v1.0/stations <br/>"
        "/api/v1.0/tobs <br/>"
        "/api/v1.0/<start><br/>"
        "/api/v1.0/<start>/<end> <br/>"
    )
# define precipitation route
@app.route('/api/v1.0/precipitation')
 def precipitation():
    print("Server accessed the Precipitation route")



# define stations route

# define tobs route

# define start/ end routes

#define the main function
if __name__ == "__main__":
    app.run(debug=True)