# from app.data_analysis.graphing import bokeh_worker, filtered_graphs
# from threading import Thread
from app import app
from flask_cors import CORS
# from app.webex.variables import webex_bot as bot
# import app.webex.teams_functions as teams_functions
# import time
# import json


# from sqlalchemy import create_engine
# engine = create_engine('postgres://qeirlxsntkwbkn:4a53f53c6fd6d1b91f30a520a97e821364ca2c71b94c67711d2e5aaaced2c6dc@ec2-54-247-79-178.eu-west-1.compute.amazonaws.com:5432/ddqb75j223tb8c')

# def trigger_bot():
#     while True: 
#         temp1 = list(engine.execute("SELECT temperature FROM telemetry_data_table ORDER BY id DESC LIMIT 10"))[0][0]
#         temp2 = list(engine.execute("SELECT temperature FROM telemetry_data_table ORDER BY id DESC LIMIT 10"))[9][0]

#         print("t1:" + str(temp1))
#         print("t2:" + str(temp2))

#         if temp1 > 29 and temp2 < 29:
#             rooms = teams_functions.list_rooms(bot.token)
#             data = rooms.json()['items']
#             for r in data:
#                 teams_functions.post_message_markdown("The Bee Hive temperature is now above 15 °C", r['id'], bot.token)
#         time.sleep(9)
        


if __name__ == "__main__":
    # Thread(target=trigger_bot).start()
    cors = CORS(app, resources={r"/dashboard/": {"origins": "diyartest.herokuapp.com"}})
    app.run(debug=False, port=5000)