"""https://www.influxdata.com/blog/getting-started-python-influxdb/"""
"""http://localhost:8086/orgs/d3cf7dd0f1213a5e/load-data/client-libraries/python"""
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

import serial

#   ['battery', 'lat', 'lon', 'height', 'time', 'alt', 'vx',
#           'vy', 'vz', 'ax', 'ay', 'az', 'mx', 'my', 'mz' ]

#defining the order of the packets to be sent
packet_indices = [
    "battery",
    "latitude",
    "longitude",
    "height",
    "time",
    "altitude",
    "velocity_X",
    "velocity_Y",
    "velocitY_Z",
    "acceleration_X",
    "acceleration_Y",
    "acceleration_Z",
    "magnetometer_X",
    "magnetometer_Y",
    "magnetometer_Z"
]

## generaitng format string from indices
fstring = "telemetry "
for i, var in enumerate(packet_indices):
    fstring += var + "={{{0}}},".format(i)
fstring = fstring[:-1]

# setting up serial connection
port = "/dev/cu.usbmodem1201"
rate = 115200
ser = serial.Serial(port, rate, timeout=1)

# You can generate an API token from the "API Tokens Tab" in the UI
token = "oNWe8ptCt_3Lx2_8Oc2oaG79yC-1-j2E5JpA9s-_agMsqKj7aTFsQ8MSEWhNlolQlLyz9i0NJzmk0oHvKQ2riA=="
org = "CPSS"
bucket = "CPSS-telemetry"

def relay_data():
    """ Loads data from serial port into Influx Database"""
    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        while True:
            # getting serial data
            line =  ser.readline()
            vars = [ float(v) for v in line.split(b',')[:-1] ]

            if (vars):
                log = fstring.format(*vars)
                write_api.write(bucket, org, log)

                # log = "telemetry acceleration={0},speed={1},temperature={2}".format(vars[0], vars[1], vars[2])
                # print(log)
                # write_api.write(bucket, org, log)
                # query = 'from(bucket: "CPSS-telemetry") |> range(start: -1h)'
                # tables = client.query_api().query(query, org=org)
                # for table in tables:
                #     for record in table.records:
                #         print(record)

            time.sleep(1)

if __name__ == "__main__":
    relay_data()