# Import the dependencies.
from flask import Flask
import numpy as np 
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station




# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
          f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
                             )

@app.route("/api/v1.0/precipitation")
def precipitation():
   
 session = Session(engine)

results = session.query(Measurement.date,Measurement.prcp).all()

session.close()

all_prcp=[]
for date,prcp in results:
    prcp_dict = {}
    prcp_dict[date] = prcp
    all_prcp.append(prcp_dict)
return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
   
   session = Session(engine)

   results = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
   session.close()
   all_station=[]
   for id,station,name,latitude,longitude,elevation in results:
        station_dict={}
        station_dict['Id']=id
        station_dict['station']=station
        station_dict['name']=name
        station_dict['latitude']=latitude
        station_dict['longitude']=longitude
        station_dict['elevation']=elevation
        all_station.append(station_dict)
   return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tempartureobs():

    session = Session(engine)


    results_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    datestart=list(np.ravel(results_date))[0]
    latest_date=dt.datetime.strptime(datestart,"%Y-%m-%d")
    date_from_lastyear=latest_date-dt.timedelta(days=366)

    results=session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).\
            filter(Measurement.date>=date_from_lastyear).all()
    session.close()
    alltemps=[]
    for tobs,date in results:
        tobs_dict={}
        tobs_dict['date']=date
        tobs_dict['tobs']=tobs
        alltemps.append(tobs_dict)
    return jsonify(alltemps)


@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):
   
    session = Session(engine)
   
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    tempobs={}
    tempobs["Min_Temp"]=results[0][0]
    tempobs["avg_Temp"]=results[0][1]
    tempobs["max_Temp"]=results[0][2]
    return jsonify(tempobs)

@app.route("/api/v1.0/<start>")
def calc_temps_sd(start):

    session = Session(engine)
    
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    session.close()
    tempobs={}
    tempobs["Min_Temp"]=results[0][0]
    tempobs["avg_Temp"]=results[0][1]
    tempobs["max_Temp"]=results[0][2]
    return jsonify(tempobs)
if __name__ == '__main__':
    app.run(debug=True)



