"""
Simple example receiving messages from the dongle and passing them to a ZeroMQ
for deliver.

May be used to distribute messages to several subscribers.
"""

import datetime
import sys

import zmq  # external dependency

from device import Device


if __name__ == "__main__":
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://127.0.0.1:33224")
    if len(sys.argv) <= 1:
        device_name = "/dev/ttyUSB0"
    else:
        device_name = sys.argv[1]
    device = Device(device_name)
    reader = device.gen_lines()
    while True:
        line = reader.next()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        publisher.send_json((date, line))
        print line
