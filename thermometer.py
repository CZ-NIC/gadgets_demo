"""
Demo of simple thermometer page using TURRIS:DONGLE and TP-82N thermometer.

The program listens to signals from a connected thermometer and stores
the values into a CSV file.

You can view the output in your browser using the thermometer.html page
which contains javascript to display data from the CSV.

NOTE: Please note that the thermometer sends signals only about each
9 minutes, so you will have to wait to gather some data. Pressing the
rotating button on the thermometer will force messages to be sent immediately.
"""

from __future__ import print_function

import re
import sys
import datetime
from time import time

from device import Device

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        device_name = "/dev/ttyUSB0"
    else:
        device_name = sys.argv[1]
    print("Using '{0}' as input device".format(device_name), file=sys.stderr)
    device = Device(device=device_name)
    reader = device.gen_lines()
    # we keep the output file open and flush it after each write
    with file("thermometer.csv", "w") as outfile:
        outfile.write("date,temperature\n")
        while True:
            line = reader.next()
            print(line)
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            m = re.search("^\[(\d{8})\].+INT:(....)", line)
            if m:
                thermometer_id, temp = m.groups()
                outfile.write("{0},{1}\n".format(date, temp))
                print("{0}: {1}".format(date, temp), file=sys.stderr)
            outfile.flush()


