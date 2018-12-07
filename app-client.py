#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libclient

sel = selectors.DefaultSelector()


<<<<<<< HEAD
def create_request(action, value):
=======
def create_request(action, value, arg):
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
    if action == "search":
        return dict(
            type="text/json",
            encoding="utf-8",
<<<<<<< HEAD
            content=dict(action=action, value=value),
=======
            content=dict(action=action, value=value, arg=arg),
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
<<<<<<< HEAD
            content=bytes(action + value, encoding="utf-8"),
=======
            content=bytes(action + value + arg, encoding="utf-8"),
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
        )


def start_connection(host, port, request):
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)


<<<<<<< HEAD
if len(sys.argv) != 5:
    print("usage:", sys.argv[0], "<host> <port> <action> <value>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
action, value = sys.argv[3], sys.argv[4]
request = create_request(action, value)
=======
if len(sys.argv) != 6:
    print("usage:", sys.argv[0], "<host> <port> <action> <value> <arg>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
action, value, arg = sys.argv[3], sys.argv[4], sys.argv[5]
request = create_request(action, value, arg)
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
start_connection(host, port, request)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
            except Exception as e:
                print(
                    "main: error: exception for",
<<<<<<< HEAD
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
=======
                    f"{message.addr}:\n{traceback.format_exc()}")
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
                message.close()
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()