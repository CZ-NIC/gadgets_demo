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

``net_echo.py``
    Listens to messages received by the dongle and passes them to given IP addresses in
    UDP datagrams. ``net_collect.py`` may be used to capture the messages.

``net_collect.py``
    Simple client which receives messages sent by ``net_echo.py`` as UDP datagrams and prints
    them out.

``thermometer.py``
    Collect temperature measurements from a TP-82N thermometer and store them in a CSV file
    ``thermometer.csv``. Also uses ``thermometer.html`` which may be used to display the
    collected data in a simple but nice JavaScript chart.

``zeromq_echo.py``
    Another simple echo client. This time it uses ZeroMQ (a very nice broker-less message queue
    for message transport). See ``zeromq_collect.py`` for more details.

    Requires the pyzmq external library.

``zeromq_collect.py``
    ZeroMQ client receiving data from ``zeromq_echo.py``. Serves as a demo of an application
    where the messages may be distributed to several clients, courtesy of ZeroMQ.

    Requires the pyzmq external library.

``device.py``
    Not a demo in itself. This is a simple communication library which is used by the other
    demos.


How to configure Turris for the dongle
--------------------------------------

The TURRIS:DONGLE uses an USB to serial converter from FTDI. Because of this, the required
kernel module must be installed for the communication to work and the /dev/ttyUSBx device
to appear.

The module to install is ``kmod-usb-serial-ftdi``. You can do it from the command line::

    opkg install kmod-usb-serial-ftdi
