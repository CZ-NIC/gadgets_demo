===================
TURRIS:GADGETS demo
===================

Code in this repository is related to the `TURRIS:GADGETS`_ project.
It is written in Python, which is available by default on router Turris.

.. _TURRIS:GADGETS: http://www.turris.cz/gadgets


Demos
-----

``gadget_command.py``
    Send individual commands to the TURRIS:DONGLE using this utility. You can use it to register
    individual sensors with the dongle.

``gadget_echo.py``
    Listen to messages received by the dongle.

``thermometer.py``
    Collect temperature measurements from a TP-82N thermometer and store them in a CSV file
    ``thermometer.csv``. Also uses ``thermometer.html`` which may be used to display the
    collected data in a simple but nice JavaScript chart.

``device.py``
    Not a demo in itself. This is a simple communication library which is used by the other
    demos.
