import serial.tools.list_ports
import configparser
import argparse

def get_cfg():
    """ Gets configuration from config file and command line args"""
    # parsing command line args
    parser = argparse.ArgumentParser(description='Receives telemetry data from OMNIS and sends it to InfluxDB')
    parser.add_argument('-c', '--cfg', type=str, default='telem.cfg')
    parser.add_argument('-l', '--logfile', type=str, default='telem.log')
    parser.add_argument('-p', '--port', type=str, default=None,
                        help='Serial port to use')
    parser.add_argument('-r', '--rate', type=int, default=None,
                        help='Baud rate to use')
    parser.add_argument('-t', '--token', type=str, default=None,
                        help='Token to use')
    parser.add_argument('-o', '--org', type=str, default=None,
                        help='Org to use')
    parser.add_argument('-b', '--bucket', type=str, default=None,
                        help='Bucket to use')
    parser.add_argument('-u', '--url', type=str, default=None,
                        help='URL to use')
    args = parser.parse_args()

    # reading config file for settings
    config = configparser.ConfigParser()
    config.read(args.cfg)

    # setting defaults if unconfigured
    args.url = args.url or config['DEFAULT']['url']
    args.token = args.token or config['DEFAULT']['token']
    args.org = args.org or config['DEFAULT']['org']
    args.bucket = args.bucket or config['DEFAULT']['bucket']
    args.rate = args.rate or config['DEFAULT']['rate']
    args.port = args.port or get_port()

    return args

def get_port():
    """ Gets the serial port from the config file """
    print("\nAvailable ports:")
    ports = serial.tools.list_ports.comports()
    for i, port in enumerate(ports):
        print("[{}] {}".format(i, port.device))
    port = int(input("\nEnter port number: "))
    return ports[port].device