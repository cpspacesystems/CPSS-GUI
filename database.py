"""https://www.influxdata.com/blog/getting-started-python-influxdb/"""
"""http://localhost:8086/orgs/d3cf7dd0f1213a5e/load-data/client-libraries/python"""
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

## NOT STABLE ##

# You can generate an API token from the "API Tokens Tab" in the UI
token = "oNWe8ptCt_3Lx2_8Oc2oaG79yC-1-j2E5JpA9s-_agMsqKj7aTFsQ8MSEWhNlolQlLyz9i0NJzmk0oHvKQ2riA=="
org = "CPSS"
bucket = "CPSS-telemetry"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)

    while True:
        acc = random.random()
        speed = int( random.random() * 10 )
        temp = random.random()

        log = "telemetry acceleration={0},speed={1},temperature={2}".format(acc, speed, temp)

        write_api.write(bucket, org, log)

        # query = 'from(bucket: "CPSS-telemetry") |> range(start: -1h)'
        # tables = client.query_api().query(query, org=org)
        # for table in tables:
        #     for record in table.records:
        #         print(record)
        time.sleep(0.1)
