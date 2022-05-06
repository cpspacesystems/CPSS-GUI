"""https://www.influxdata.com/blog/getting-started-python-influxdb/"""
"""http://localhost:8086/orgs/d3cf7dd0f1213a5e/load-data/client-libraries/python"""
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

import time
import serial

from util import get_cfg

#defining the order of the packets to be sent
PACKETS = [
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
for i, var in enumerate(PACKETS):
    fstring += var + "={{{0}}},".format(i)
fstring = fstring[:-1]

print(fstring)

def relay_data(cfg):
    """ Loads data from serial port into Influx Database"""
    # setting up serial connection
    ser = serial.Serial(cfg.port, cfg.rate, timeout=1)

    with InfluxDBClient(url=cfg.url, token=cfg.token, org=cfg.org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        while True:
            # getting serial data
            line =  ser.readline()
            vars = [ float(v) for v in line.split(b',')[:-1] ]
            print(vars)
            if (vars):
                log = fstring.format(*vars)
                write_api.write(cfg.bucket, cfg.org, log)

            time.sleep(1)

if __name__ == "__main__":
    cfg = get_cfg()
    relay_data(cfg)