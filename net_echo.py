import datetime
import socket
import sys

from device import Device


def send_message(addr, port, message, date=None):
    addr_info = socket.getaddrinfo(addr, port, 0, 0, socket.IPPROTO_UDP)
    if addr_info:
        family, socktype, proto, canonname, sockaddr = addr_info[0]
        sock = socket.socket(family, socket.SOCK_DGRAM)
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sock.sendto(date+"|"+message, sockaddr)
    else:
        raise Exception("Cannot process address {0}".format(addr))


if __name__ == "__main__":
    ADDRS = [("localhost", 33223)]  # where to send the data
    if len(sys.argv) <= 1:
        device_name = "/dev/ttyUSB0"
    else:
        device_name = sys.argv[1]
    device = Device(device_name)
    reader = device.gen_lines()
    while True:
        line = reader.next()
        for addr, port in ADDRS:
            send_message(addr, port, line)
            print line
