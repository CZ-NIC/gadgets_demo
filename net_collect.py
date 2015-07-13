"""
Simple listener which receives UDP packets containing messages from
net_echo.py and prints them out.
"""

import socket
import select
import sys


class RemoteDevice(object):
    """
    Implements the device.Device interface but uses UDP datagrams to receive
    data.
    """

    def __init__(self, addr=None, port=33223):
        """
        :param addr: str, when None, address is autodetected
        :param port: int
        """
        if not addr:
            addr = socket.getfqdn()
        addr_infos = socket.getaddrinfo(addr, port)
        seen_sockaddrs = set()  # used to detect and skip duplicates
        # open sockets for all detected addresses
        self.sockets = []
        for addr_info in addr_infos:
            family, socktype, proto, canonname, sockaddr = addr_info
            if sockaddr in seen_sockaddrs:
                continue
            sock = socket.socket(family, socket.SOCK_DGRAM)
            sock.bind(sockaddr)
            self.sockets.append(sock)
            seen_sockaddrs.add(sockaddr)

    def gen_lines(self):
        while True:
            rdbs, wtbs, xtbs = select.select(self.sockets, [], [])
            if rdbs:
                for rdb in rdbs:
                    data = rdb.recv(1024)
                    yield data


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        address = "localhost"
    else:
        address = sys.argv[1]
    device = RemoteDevice(addr=address)
    reader = device.gen_lines()
    while True:
        line = reader.next()
        date, message = line.split("|")
        print date, message

