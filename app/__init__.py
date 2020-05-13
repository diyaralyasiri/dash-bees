from flask import Flask
from flask_mqtt import Mqtt
from app.data_analysis.SQL_helper_functions import Store_Telemetry_Data
import json
import app.webex.webhook_functions as functions
from flask_sqlalchemy import SQLAlchemy
from app.webex.variables import webex_bot as bot
import app.webex.teams_functions as teams_functions
from sqlalchemy import create_engine
engine = create_engine('postgres://qeirlxsntkwbkn:4a53f53c6fd6d1b91f30a520a97e821364ca2c71b94c67711d2e5aaaced2c6dc@ec2-54-247-79-178.eu-west-1.compute.amazonaws.com:5432/ddqb75j223tb8c')


# buffer1=0
# buffer2=0

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
   
    temp1 = list(engine.execute("SELECT temperature FROM telemetry_data_table ORDER BY id DESC LIMIT 7"))[0][0]
    temp2 = list(engine.execute("SELECT temperature FROM telemetry_data_table ORDER BY id DESC LIMIT 7"))[6][0]

    print("t1:" + str(temp1))
    print("t2:" + str(temp2))

    if temp1 > 26 and temp2 < 26:
        rooms = teams_functions.list_rooms(bot.token)
        data = rooms.json()['items']
        for r in data:
            teams_functions.post_message_markdown("The Bee Hive temperature is now above 15 °C", r['id'], bot.token)

    
    Store_Alchemy(data)


from app.views import views

# print ("Initializing Webhooks...")

# token = "ZWVhZTdiMzctZTAyZS00N2Y4LTgwZTktMDVjZWE4MDg0N2E2MWNkMGRmZTYtNjMz_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
# url = "https://apis-mellifera.herokuapp.com/"

# functions.delete_wehbook(functions.list_webhook(token), token)
# functions.create_webhook_new_message(url, token)
# functions.create_webhook_new_room(url, token)

# print ("$$$$$  Webhooks initialized  $$$$$")
