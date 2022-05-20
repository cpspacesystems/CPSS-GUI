"""https://www.influxdata.com/blog/getting-started-python-influxdb/"""
"""http://localhost:8086/orgs/d3cf7dd0f1213a5e/load-data/client-libraries/python"""
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

import serial
import logging

from util import get_cfg

#defining the order of the items in packet to be sent
PACKET_ITEMS = [
    "id",
    "pressure",
    "ASL",
    "AGL",
    "smoothAGL",
    "temperature",
    "accelX",
    "accelY",
    "accelZ",
    "gyroX",
    "gyroY",
    "gyroZ",
    "velocityX",
]
## generaitng format string from indices
fstring = "telemetry "
for i, var in enumerate(PACKET_ITEMS):
    fstring += var + "={{{0}}},".format(i)
fstring = fstring[:-1]

# for calculating packet loss
def relay_data(cfg):
    """ Loads data from serial port into Influx Database"""
    first_id = -1 ## the id of the first packet sent
    total_packets = 0
    sent_packets = 0

    # setting up serial connection
    with serial.Serial(cfg.port, cfg.rate, timeout=1) as ser:
        # Setting up InfluxDB client
        with InfluxDBClient(url=cfg.url, token=cfg.token, org=cfg.org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)

            while True:
                # getting serial data
                try:
                    line =  ser.readline()
                    total_packets += 1
                except Exception:
                    logger.error("Serial connection lost. Reconnecting...")
                    # trying to connect again
                    try:
                        ser = serial.Serial(cfg.port, cfg.rate, timeout=1)
                    except Exception:
                        logger.critical("Could not reconnect. Exiting...")
                        return

                # parsing serial data
                try:
                    vars = [ float(v) for v in line.split(b',')]
                    vars[0] = int(vars[0]) #id
                except ValueError as e:
                    logger.warning("{0}:{1}".format(line, e))
                    vars = []

                # sending data to influx
                if (vars and len(vars) == len(PACKET_ITEMS)):
                    # calculating packet drop (last id - first id)
                    if( first_id == -1 ):
                        first_id = vars[0]
                    total_packets = vars[0] - first_id + 1

                    log = fstring.format(*vars)
                    # writing sensor data
                    write_api.write(cfg.bucket, cfg.org, log)
                    # writing status data
                    lost = total_packets - sent_packets
                    write_api.write(cfg.bucket, cfg.org,
                        "telemetry percent_dropped={}".format(lost/total_packets))
                    sent_packets += 1
                    logger.info(log)
                else:
                    lost = total_packets - sent_packets
                    logger.warning("Bad data. Total Loss: {} packets".format(lost))
                    logger.debug("Expected {} items, got {}. Received: {}".format(len(PACKET_ITEMS), len(vars), vars))

if __name__ == "__main__":
    cfg = get_cfg()

    # logging.basicConfig(filename = cfg.logfile)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(cfg.logfile)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    relay_data(cfg)
    logging.shutdown()