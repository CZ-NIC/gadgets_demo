"""
Simple demo for sending commands to the TURRIS:DONGLE.

It can be used for sensor registration, etc.::

    >> python gadget_command.py "GET SLOT:01"
    SENDING: GET SLOT:01
    REPLY: SLOT:01 [07473725]


    >> python gadget_command.py SET SLOT:03 [07439975]
    SENDING: SET SLOT:03 [07439975]
    REPLY: OK
"""

import sys

from device import Device

if __name__ == "__main__":
    device = Device(device="/dev/ttyUSB1")
    reader = device.gen_lines(timeout=20)
    for c in sys.argv[1:]:
        print "SENDING:", c
        device.send_command(c)
        print "REPLY:", reader.next()
