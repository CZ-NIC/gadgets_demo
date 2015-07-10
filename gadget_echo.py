"""
Simple demo of reading messages from the TURRIS:DONGLE.

Just run it from the command line and watch the messages printed
on the standard output.
"""

from __future__ import print_function
import sys
import datetime

from device import Device

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        device_name = "/dev/ttyUSB0"
    else:
        device_name = sys.argv[1]
    print("Using '{0}' as input device".format(device_name), file=sys.stderr)
    device = Device(device=device_name)
    reader = device.gen_lines()
    while True:
        line = reader.next()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(date, line)
