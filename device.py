import termios
import os
import select
import time

class Device(object):

    """Simple interface to the TURRIS:DONGLE"""

    def __init__(self, device="/dev/ttyUSB0"):
        self.device = device
        self.fd = self.open_device(self.device)
        self._buffer = ""

    @classmethod
    def open_device(cls, device):
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
        os.write(self.fd, "\n"+command+"\n")
