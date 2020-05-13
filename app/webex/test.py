
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import requests
from sqlalchemy import create_engine
engine = create_engine('postgres://qeirlxsntkwbkn:4a53f53c6fd6d1b91f30a520a97e821364ca2c71b94c67711d2e5aaaced2c6dc@ec2-54-247-79-178.eu-west-1.compute.amazonaws.com:5432/ddqb75j223tb8c')
import time 


token = "OGVlMjQ1MDQtODU1Yy00YTMzLWFjN2UtM2QyMTdhZDc4YWY1MThhYWViMDQtNTZk_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"

def list_rooms(token):
    """
    Lists all of the rooms available to the given token.
    Returns a JSON-encoded response.
    """

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    headers = {'Authorization': 'Bearer ' + token,
               'Content-Type': 'application/json'}
    resp = requests.get('https://api.ciscospark.com/v1/rooms',
                        verify=False, headers=headers)

    return resp

def post_message_markdown(message_text, room_id, token):
    """
    Posts the message_text as markdown format to the Spark room with the ID of room_id using the token.
    Returns the JSON-encoded response.
    """

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    headers = {'Accept': 'application/json',
               'Authorization': 'Bearer ' + token,
               'Content-Type': 'application/json'}

    body = json.dumps({'roomId': room_id, 'markdown': message_text})

    resp = requests.post('https://api.ciscospark.com/v1/messages', headers=headers, data=body)

    return resp

n=5

while n>0:

    temp1 = list(engine.execute("SELECT temperature FROM telemetry_data_table ORDER BY id DESC LIMIT 5"))[0][0]
    temp2 = list(engine.execute("SELECT temperature FROM telemetry_data_table ORDER BY id DESC LIMIT 5"))[4][0]

    print("t1:" + str(temp1))
    print("t2:" + str(temp2))

    if temp1 > 26 and temp2 < 26:
        rooms = list_rooms(token)
        data = rooms.json()['items']
        for r in data:
            post_message_markdown("The Bee Hive temperature is now above 15 °C", r['id'], token)

    time.sleep(10)