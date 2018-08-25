# Import dependencies
import pandas as pd
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Station(Base):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    station_id = Column(Integer)
    name = Column(String)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    dpcapacity = Column(Integer)
    online_date = Column(String)

class Trip(Base):
    __tablename__ = 'trip'
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer)
    start_time = Column(String)
    end_time = Column(String)
    tripduration = Column(Integer)
    from_station_id = Column(Integer)
    to_station_id = Column(Integer)
    usertype = Column(String)
    gender = Column(String)
    birthyear = Column(Integer)


# Create our database engine
engine = create_engine('sqlite:///db/divvy.sqlite')

# This is where we create our tables in the database
Base.metadata.create_all(engine)

# The ORM’s “handle” to the database is the Session.
session = Session(engine)

# Read in the data using pandas
stations_df = pd.read_csv('data/Divvy_Stations_2017_Q3Q4.csv')
trips_df = pd.read_csv('data/Divvy_Trips_2017_Q4.csv')


# Loop through the DFs and add each element to the session then commit to the SQLite engine
for index, row in stations_df.iterrows():
    session.add(Station(station_id=row[0],
                            name = row[1],
                            latitude = row[3],
                            longitude = row[4],
                            dpcapacity = row[5],
                            online_date = row[6]))

session.commit()

for index, row in trips_df.iterrows():
    session.add(Trip(trip_id = row[0],
                            start_time = row[1],
                            end_time = row[2],
                            tripduration = row[4],
                            from_station_id = row[5],
                            to_station_id = row[7],
                            usertype = row[9],
                            gender = row[10],
                            birthyear = row[11])) 

session.commit()