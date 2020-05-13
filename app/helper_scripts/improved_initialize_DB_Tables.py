# Script for creating or connecting to Database

import sqlite3

# SQLite DB Name
DB_Name =  "Bee_Telemetry_Database.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists Telemetry_Data_Table ;
create table Telemetry_Data_Table (
  id integer primary key autoincrement,
  Timestamp datetime,
  Temperature float,
  Wieght float,
  Humidity float
);
CREATE INDEX index_name ON Telemery_Data_Table (Timestamp);
"""
#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
curs.close()
conn.close()