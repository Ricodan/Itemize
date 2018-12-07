#!/usr/bin/env python3
<<<<<<< HEAD
import sys
import selectors
import socket
import types

sel = selectors.DefaultSelector()
=======

import sys
import socket
import selectors
import types
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5

sel = selectors.DefaultSelector()

<<<<<<< HEAD
#host = '127.0.0.1'
#port = 65432

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print("accepted connection from:", addr)
=======
welcome = "Welcome to Itemize!\nFunctions:\ncreate_new_list(name_of_list)\nedit_list(name_of_list)\nshow_lists()\nEnter your function:"

def accept_wrapper(sock):
    conn, addr = sock.accept()  # lsocket Should be ready to read
    print("accepted connection from", addr)
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=welcome.encode())
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
<<<<<<< HEAD
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
=======
    if mask & selectors.EVENT_READ: # if server is going to read data
        recv_data = sock.recv(1024).decode()  # Should be ready to read
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
        if recv_data:
            print("received", str(recv_data), "from connection", data.connid)
            # now we have received stuff and we append this to outbound data
            data.outb += recv_data
<<<<<<< HEAD
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("echoing", repr(data.outb), "to", data.addr)
=======
        else:   # if we did not receive data from client - then close connection
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:    # if server is sending stuff
        if data.outb:
            # since we appended stuff to field data.outbound, we are now going to send it
            print("sending", repr(data.outb), "to", data.addr)
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

<<<<<<< HEAD

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
=======
host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
# we have registrered the lsock as read

<<<<<<< HEAD
=======
list = ['apples', '2 bananas', 'oranges']

>>>>>>> 2d7c40dc6d03301a5e24e2fc066db8f4006042c5
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()

