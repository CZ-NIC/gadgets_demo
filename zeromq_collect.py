"""
Simple listener using ZeroMQ (0MQ) message queue to receive messages
"""

import zmq  # external dependency

if __name__ == "__main__":
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://127.0.0.1:33224")
    subscriber.setsockopt(zmq.SUBSCRIBE, "")
    while True:
        date, message = subscriber.recv_json()
        print date, message
