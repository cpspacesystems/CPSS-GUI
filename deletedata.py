"""https://www.influxdata.com/blog/getting-started-python-influxdb/"""
"""http://localhost:8086/orgs/d3cf7dd0f1213a5e/load-data/client-libraries/python"""
from datetime import datetime
from influxdb import DataFrameClient


# You can generate an API token from the "API Tokens Tab" in the UI
token = "oNWe8ptCt_3Lx2_8Oc2oaG79yC-1-j2E5JpA9s-_agMsqKj7aTFsQ8MSEWhNlolQlLyz9i0NJzmk0oHvKQ2riA=="
org = "CPSS"
bucket = "CPSS-telemetry"

start = datetime.fromisocalendar(year=2020, week=1, day=1)
stop = datetime.now()

client = DataFrameClient(host="localhost", port=8086, username="admin", password="password", database=bucket)
client.drop_database(bucket)