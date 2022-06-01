"""https://www.influxdata.com/blog/getting-started-python-influxdb/"""
"""http://localhost:8086/orgs/d3cf7dd0f1213a5e/load-data/client-libraries/python"""
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

import serial
import logging

from util import get_cfg

# for uplink
import uplink.uplink as uplink
""" Serial connection lost. Reconnecting...
Traceback (most recent call last):
  File "/Users/curtisbucher/Desktop/Clubs/CPSS-GUI/telemetry.py", line 126, in <module>
    main()
  File "/Users/curtisbucher/Desktop/Clubs/CPSS-GUI/telemetry.py", line 69, in main
    relay_data(cfg, logger, write_api, ser, )
  File "/Users/curtisbucher/Desktop/Clubs/CPSS-GUI/telemetry.py", line 98, in relay_data
    vars = [ float(v) for v in line.split(b',')]
UnboundLocalError: local variable 'line' referenced before assignment"""

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

# TODO: Make not global
first_id = -1 ## the id of the first packet sent
total_packets = 0
sent_packets = 0

def main():
    """ Main function """
    cfg = get_cfg()

    # Loading logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Setting up console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logger.addHandler(console_handler)

    # Setting up file handler
    file_handler = logging.FileHandler(cfg.logfile, mode='w')
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # Starting uplink

    # setting up serial connection
    with serial.Serial(cfg.port, cfg.rate, timeout=1) as ser:
        # Setting up InfluxDB client
        with InfluxDBClient(url=cfg.url, token=cfg.token, org=cfg.org) as client:
            logger.info("Starting telemetry relay")
            write_api = client.write_api(write_options=SYNCHRONOUS)
            try:
                while( True ):
                    relay_data(cfg, logger, write_api, ser, )

            except KeyboardInterrupt:
                logger.info("\nExiting...")
                logging.shutdown()

# for calculating packet loss
def relay_data(cfg, logger=None, db_write_api=None, ser=None):
    """ Loads data from serial port into Influx Database"""
    #TODO: Make not global
    global total_packets
    global sent_packets
    global first_id

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
        db_write_api.write(cfg.bucket, cfg.org, log)
        # writing status data
        lost = total_packets - sent_packets
        db_write_api.write(cfg.bucket, cfg.org,
            "telemetry percent_dropped={}".format(lost/total_packets))
        sent_packets += 1
        logger.info(log)
    else:
        lost = total_packets - sent_packets
        logger.warning("Bad data. Total Loss: {} packets".format(lost))
        logger.debug("Expected {} items, got {}. Received: {}".format(len(PACKET_ITEMS), len(vars), vars))

if __name__ == "__main__":
    main()