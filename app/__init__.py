from flask import Flask
from flask_mqtt import Mqtt
from app.data_analysis.SQL_helper_functions import Store_Telemetry_Data
import json
import app.webex.webhook_functions as functions

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mqtt.eclipse.org'
app.config['MQTT_BROKER_PORT'] = 1883
mqtt = Mqtt(app)

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

    Store_Telemetry_Data(data)


from app.views import views

# print ("Initializing Webhooks...")

# token = "ZWVhZTdiMzctZTAyZS00N2Y4LTgwZTktMDVjZWE4MDg0N2E2MWNkMGRmZTYtNjMz_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
# url = "https://apis-mellifera.herokuapp.com/"

# functions.delete_wehbook(functions.list_webhook(token), token)
# functions.create_webhook_new_message(url, token)
# functions.create_webhook_new_room(url, token)

# print ("$$$$$  Webhooks initialized  $$$$$")
