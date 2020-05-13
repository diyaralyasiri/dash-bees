from sqlalchemy import create_engine
engine = create_engine('postgres://qeirlxsntkwbkn:4a53f53c6fd6d1b91f30a520a97e821364ca2c71b94c67711d2e5aaaced2c6dc@ec2-54-247-79-178.eu-west-1.compute.amazonaws.com:5432/ddqb75j223tb8c')

result_set = engine.execute("SELECT timestamp FROM telemetry_data_table ORDER BY id DESC LIMIT 1")

print(type(list(result_set)[0][0]))