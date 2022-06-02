#!/bin/bash
docker start influxdb
open "http://localhost:8086"
python3 /Users/CPSS/Desktop/CPSS-GUI/telemetry.py
