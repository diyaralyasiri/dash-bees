from flask import Flask
from flask_mqtt import Mqtt
from app.data_analysis.SQL_helper_functions import Store_Telemetry_Data
import json
import app.webex.webhook_functions as functions
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mqtt.eclipse.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qeirlxsntkwbkn:4a53f53c6fd6d1b91f30a520a97e821364ca2c71b94c67711d2e5aaaced2c6dc@ec2-54-247-79-178.eu-west-1.compute.amazonaws.com:5432/ddqb75j223tb8c'
mqtt = Mqtt(app)

db = SQLAlchemy(app)

class telemetry_data_table(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    timestamp= db.Column(db.TIMESTAMP)
    temperature = db.Column(db.Float)
    weight= db.Column(db.Float)
    humidity= db.Column(db.Float)

    def __repr__(self):
        return '<Telemetry_Data_Table %r>' % self.Timestamp

# db.create_all()

def Store_Alchemy(data):
    #Parse Data
    DT = str(data['Date'])
    # print(DT)
    T = str(data['Temperature'])
    H = str(data['Humidity'])
    W = str(data['Wieght'])
    row = telemetry_data_table(timestamp=DT, temperature=T, weight=W, humidity=H )
    #Push into DB Table
    db.session.add(row)
    db.session.commit()
    # print ("Inserted Telemetry Data into Alchemy Database.")
    # print ("")

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('Connectedbees/Telemetry')
    # print("Subscribed to MQTT topic.")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    
    topic= message.topic
    data= json.loads(message.payload.decode())

    # print ("MQTT Data Received...")
    # print ("MQTT Topic: " + topic)
    # print ("Data: " + str(data))

    # if buffer 1 != null {
    #   buffer 2= data.temperature     
    # }

    # if buffer 2 > 15c && buffer 1 < 15c {
    #  unsert webhook here posts to all rooms
    # }

    # buffer 1 = data.temperagature
   
    #  data.temperate  

    Store_Alchemy(data)


from app.views import views

# print ("Initializing Webhooks...")

# token = "ZWVhZTdiMzctZTAyZS00N2Y4LTgwZTktMDVjZWE4MDg0N2E2MWNkMGRmZTYtNjMz_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
# url = "https://apis-mellifera.herokuapp.com/"

# functions.delete_wehbook(functions.list_webhook(token), token)
# functions.create_webhook_new_message(url, token)
# functions.create_webhook_new_room(url, token)

# print ("$$$$$  Webhooks initialized  $$$$$")
