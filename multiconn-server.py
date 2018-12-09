#!/usr/bin/env python3

import sys
import socket
import selectors
import types
import json

shopping_lists = {"Itemize": ["dodis"], "Christmas": ["ham", "prince sausage"], "Charity": ["bread", "butter"]}

sel = selectors.DefaultSelector()

welcome = "Welcome to Itemize!\nFunctions:\ncreate_new_list()\nedit_list()\nshow_lists()\nEnter your function:"

def send_dictionary(key, mask):

    json.dumps(shopping_lists)
    sock = key.fileobj
    data = key.data
    prompt_msg = 'Which list do you want?: '

    data.outb = prompt_msg.encode()
    if mask & selectors.EVENT_WRITE:  # if server is sending stuff
        if data.outb:
            # since we appended stuff to field data.outbound, we are now going to send it
            print("sending", str(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

            #if we want to view one list only then only that list should be sent to the client.



def accept_wrapper(sock):
    conn, addr = sock.accept()  # lsocket Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=welcome.encode())
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def create_new_list(key, mask):
    # send prompt to client to enter name of new list

    sock = key.fileobj
    data = key.data
    prompt_msg = 'Enter name of new list: '
    data.outb = prompt_msg.encode()
    if mask & selectors.EVENT_WRITE:    # if server is sending stuff
        if data.outb:
            # since we appended stuff to field data.outbound, we are now going to send it
            print("sending", str(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
    # new_list_name = input('Enter name of new list: ')
    # # append this new list to dictionary holding all lists
    # lists[new_list_name] = []
    # # send confirmation msg to client
    # sock = key.fileobj
    # data = key.data
    # confirm_msg = 'Created new list called ' + new_list_name
    # data.outb = confirm_msg.encode()
    # if mask & selectors.EVENT_WRITE:    # if server is sending stuff
    #     if data.outb:
    #         # since we appended stuff to field data.outbound, we are now going to send it
    #         print("sending", str(data.outb), "to", data.addr)
    #         sent = sock.send(data.outb)  # Should be ready to write
    #         data.outb = data.outb[sent:]

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ: # if server is going to read data
        recv_data = sock.recv(1024).decode()  # Should be ready to read
        if recv_data:
            print("received", str(recv_data), "from connection")
            # now we have received stuff and we append this to outbound data
            #data.outb += recv_data
            # look at recv_data - go to that function
            if recv_data == 'create_new_list()':
                create_new_list(key, mask)

            if recv_data == 'all_lists()':
                send_dictionary(key, mask)
        else:   # if we did not receive data from client - then close connection
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:    # if server is sending stuff
        if data.outb:
            # since we appended stuff to field data.outbound, we are now going to send it
            print("sending", repr(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
# we have registrered the lsock as read

list = ['apples', '2 bananas', 'oranges']

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