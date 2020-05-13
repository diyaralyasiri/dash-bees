from app import app
from flask import render_template, request, redirect
from werkzeug.utils import secure_filename
from app.data_analysis.SQL_helper_functions import DatabaseManager
from app.webex.variables import webex_bot as bot
import app.webex.teams_functions as teams_functions

from bokeh.embed import server_document, components
from flask import render_template
import os

from app.data_analysis.graphing import  filtered_graphs, parse_input_time

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard/")
def graph():
    script = server_document("https://bokeh-bee.herokuapp.com")
    # script = server_document("https://diyartest.herokuapp.com:5006/bees")
    return render_template("dashboard.html", script=script, template="Flask")

@app.route("/filtered/", methods=['POST'])
def graph_filtered():
    starttime = request.form['start-time']
    endtime = request.form['end-time']
    t1=parse_input_time(starttime)
    t2=parse_input_time(endtime)
    print(str(starttime))
    print(str(endtime))
    plot = filtered_graphs(t1,t2)
    script, div = components(plot)
    return render_template("dashboard_filtered.html", script=script, div1=div[0], div2=div[1], div3=div[2])

@app.route('/newmessage', methods=['POST'])
def new_message():
    json_data = request.json

    message_id = json_data["data"]["id"]
    room_id = json_data["data"]["roomId"]

    message = teams_functions.get_message(message_id, bot.token)
    print(room_id)
    print(message)

    # I would like to show the operational data of my interfaces
    if message == "CaptainBuzz How's the weather?":
        dbObj = DatabaseManager()
        Latest_temp = str(dbObj.read_db_record("SELECT Temperature FROM Telemetry_Data_Table ORDER BY id DESC LIMIT 1")[0][0])
        Latest_hum = str(dbObj.read_db_record("SELECT Humidity FROM Telemetry_Data_Table ORDER BY id DESC LIMIT 1")[0][0])
        Latest_w = str(dbObj.read_db_record("SELECT Wieght FROM Telemetry_Data_Table ORDER BY id DESC LIMIT 1")[0][0])
        TimeStamp = str(dbObj.read_db_record("SELECT Timestamp FROM Telemetry_Data_Table ORDER BY id DESC LIMIT 1")[0][0])
        print("Temperature= " + Latest_temp + ' °C Humidity= ' + Latest_hum + ' % Weight= ' + Latest_w +' % Time Stamp: ' + TimeStamp[:20])
        teams_functions.post_message_markdown((
                "I was hoping you'd ask me that! The current conditions in the hive are:<br/>Temp= " + Latest_temp + ' °C<br/>Humidity= ' + Latest_hum + ' °%<br/>Weight= ' + Latest_w +' Kg<br/>Time Stamp: ' + TimeStamp[:20]), room_id, bot.token)
        del dbObj
    else:
        teams_functions.post_help_bot(room_id, bot.token)
    return "message sent"

@app.route('/newroom', methods=['POST'])
def new_room():
    json_data = request.json

    room_id = json_data["data"]["roomId"]
    print(room_id)
    teams_functions.post_message_markdown("Hey, I have been added to a new room !", room_id, bot.token)
    teams_functions.post_help_bot(room_id, bot.token)

    return "message sent"
