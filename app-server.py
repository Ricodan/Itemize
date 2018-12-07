#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libserver

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
<<<<<<< HEAD
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


=======
    print('create a instance of Message')
    message = libserver.Message(sel, conn, addr)
    print('set event to read from client on this socket')
    sel.register(conn, selectors.EVENT_READ, data=message)

print('in server code')
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
<<<<<<< HEAD
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
=======
                print('no data sent, client trying to connect')
                accept_wrapper(key.fileobj)
            else:
                print('this data from client is put into message')
                message = key.data
                try:
                    print('process the mess')
                    message.process_events(mask)
                except Exception:
                    print("main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}")
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
                    message.close()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()