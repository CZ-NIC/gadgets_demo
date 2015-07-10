"""
Simple demo of reading messages from the TURRIS:DONGLE.

Just run it from the command line and watch the messages printed
on the standard output.
"""

import datetime

from device import Device

if __name__ == "__main__":
    device = Device(device="/dev/ttyUSB1")
    reader = device.gen_lines()
    while True:
        line = reader.next()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print date, line
