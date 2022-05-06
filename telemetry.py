"""https://www.influxdata.com/blog/getting-started-python-influxdb/"""
"""http://localhost:8086/orgs/d3cf7dd0f1213a5e/load-data/client-libraries/python"""
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

import time
import serial

from util import get_cfg

#defining the order of the items in packet to be sent
PACKET_ITEMS = [
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
for i, var in enumerate(PACKET_ITEMS):
    fstring += var + "={{{0}}},".format(i)
fstring = fstring[:-1]

# for calculating packet loss
def relay_data(cfg):
    """ Loads data from serial port into Influx Database"""
    dropped_packets = 0
    total_packets = 0

    # setting up serial connection
    ser = serial.Serial(cfg.port, cfg.rate, timeout=1)

    with InfluxDBClient(url=cfg.url, token=cfg.token, org=cfg.org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        while True:
            # getting serial data
            try:
                line =  ser.readline()
                total_packets += 1
            except Exception:
                print("Serial connection lost. Reconnecting...")
                # trying to connect again
                try:
                    ser = serial.Serial(cfg.port, cfg.rate, timeout=1)
                except Exception:
                    print("Could not reconnect. Exiting...")
                    return

            # parsing serial data
            try:
                vars = [ float(v) for v in line.split(b',')[:-1] ]
            except ValueError:
                dropped_packets+=1
                print("Packet Dropped. Total Loss: {} packets".format(dropped_packets))

            # sending data to influx
            if (len(vars) == len(PACKET_ITEMS)):
                log = fstring.format(*vars)
                # writing sensor data
                write_api.write(cfg.bucket, cfg.org, log)
                # writing status data
                write_api.write(cfg.bucket, cfg.org, "telemetry percent_dropped={}".format(dropped_packets/total_packets))
            else:
                dropped_packets += 1
                print("Packet Dropped. Total Loss: {} packets".format(dropped_packets))

            time.sleep(1)

if __name__ == "__main__":
    cfg = get_cfg()
    relay_data(cfg)