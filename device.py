import termios
import os
import select
import time

class Device(object):

    """Simple interface to the TURRIS:DONGLE"""

    def __init__(self, device="/dev/ttyUSB0"):
        """
        Initialize the TURRIS:DONGLE by opening the corresponding device
        with the proper settings.
        """
        self.device = device
        self.fd = self.open_device(self.device)
        self._buffer = ""

    @classmethod
    def open_device(cls, device):
        """
        Open the TURRIS:DONGLE device using the proper settings, such as baudrate, etc.
        """
        fd = os.open(device, os.O_RDWR)
        baudrate = termios.B57600
        # set termios flags
        newcc = termios.tcgetattr(fd)[6]
        # this causes read to be non-blocking
        newcc[termios.VMIN] = 0
        newcc[termios.VTIME] = 0
        termios.tcsetattr(fd, termios.TCSAFLUSH, [
            termios.IGNBRK,
            0,
            termios.CS8 | termios.CREAD | termios.CLOCAL | baudrate,
            0,
            baudrate,
            baudrate,
            newcc,
        ])
        termios.tcflush(fd, termios.TCIOFLUSH)
        return fd

    def gen_lines(self, timeout=None):
        """
        Generator returning individual lines received by the TURRIS:DONGLE.

        Note: Messages are sent more than once by the sensors to protect
        against data loss. This code does not take care of removing the
        duplicates, it is up to you.
        """
        start_time = time.time()
        while True:
            rdb, wtb, xtb = select.select([self.fd], [], [], timeout)
            if rdb:
                fd = rdb[0]
                data = os.read(fd, 1024)
                self._buffer += data
            if "\n" in self._buffer:
                parts = self._buffer.split("\n")
                self._buffer = parts[-1]
                for part in parts[:-1]:
                    if part and part.replace("\0", ""):
                        yield part
                        start_time = time.time()
            if timeout and time.time() - start_time > timeout:
                yield None
                start_time = time.time()

    def send_command(self, command):
        """
        Send one command to the TURRIS:DONGLE. The command should conform to
        the internal protocol of the device
        """
        os.write(self.fd, "\x1B "+command+" \n")
