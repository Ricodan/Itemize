#!/usr/bin/env python3

import sys
import socket
import selectors
import types
import json

# data representation
# dictionary of all lists: key = list name, value = list
# dictionary of all clients: key = client, value = list of all list names that client subscribes to
lists = {}
clients = {}
sel = selectors.DefaultSelector()

welcome = "Welcome to Itemize!\nFunctions:\ncreate_new_list()\nedit_list()\nshow_lists()\nPress 'm' at any time to return to this menu"

def accept_wrapper(sock):
    conn, addr = sock.accept()  # lsocket Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=welcome.encode(), show=False, sent_msg=0, set_name_fst=False, delete=False, set_name=False, edit=False, list=None, add=False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def get_list_name(key, mask):
    # send prompt to client to enter name of new list
    sock = key.fileobj
    data = key.data
    msg = 'Enter name of list: '
    data.outb = msg.encode()
    if mask & selectors.EVENT_WRITE:    # if server is sending stuff
        if data.outb:
            # since we appended stuff to field data.outbound, we are now going to send it
            print("sending", str(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

def handle_list_data(name, key, mask):
    sock = key.fileobj
    data = key.data
    if data.set_name_fst:
        # we are creating a new list with this name
        # append a new list to dictionary holding all lists
        lists[name] = []
        # append dictionary with clients
        clients[data.addr[1]] = []
        clients[data.addr[1]].append(name)
        # send confirmation msg to client
        msg = 'Created new list called ' + name
        data.outb = msg.encode()
        data.set_name_fst=False
    elif data.set_name:
        # we are creating a new list with this name
        # append a new list to dictionary holding all lists
        lists[name] = []
        # append dictionary with clients
        clients[data.addr[1]].append(name)
        # send confirmation msg to client
        msg = 'Created new list called ' + name
        data.outb = msg.encode()
        data.set_name=False
    elif data.edit:
        # we are editing the list with this name
        data.list = name
        data.edit=False
        send_edit_list_menu(key, mask)
    elif data.add:
        # var name is the item we are appending to the list
        lists[data.list].append(name)
    elif data.delete:
        # we are deleting from the list with this index (encoded as str)
        index = int(name)
        lists[data.list].pop(index-1)
    elif data.show:
        # we have to display the list with index 'name'
        index = int(name) -1
        list = clients[data.addr[1]]
        list_name = list[index]
        list_to_send = {list_name: lists[list_name]}
        data.outb = json.dumps(list_to_send).encode()
        if mask & selectors.EVENT_WRITE:  # if server is sending stuff
            if data.outb:
                # since we appended stuff to field data.outbound, we are now going to send it
                print("sending", str(data.outb), "to", data.addr)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

    if mask & selectors.EVENT_WRITE:    # if server is sending stuff
        if data.outb:
            # since we appended stuff to field data.outbound, we are now going to send it
            print("sending", str(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

def send_edit_list_menu(key, mask):
    sock = key.fileobj
    data = key.data
    edit_list_menu = "Press 'a' to add items to list\nPress 'd' to delete items from list"
    data.outb = edit_list_menu.encode()
    if mask & selectors.EVENT_WRITE:  # if server is sending stuff
        if data.outb:
            # since we appended stuff to field data.outbound, we are now going to send it
            print("sending", str(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

def send_list(key, mask):
    sock = key.fileobj
    data = key.data
    # we have to display list that we are adding to
    # we are sending a dictionary to client with key = name of list and value = list
    # dictionary is an object so serialize with JSON
    # create the dictionary we are sending to client first
    dic = {data.list: lists[data.list]}
    data.outb = json.dumps(dic).encode()
    if mask & selectors.EVENT_WRITE:  # if server is sending stuff
        if data.outb:
            # since we appended stuff to field data.outbound, we are now going to send it
            print("sending", str(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

def get_lists(key, mask):
    sock = key.fileobj
    data = key.data
    client_id = data.addr[1]
    list = clients[client_id]
    data.outb = json.dumps(list).encode()
    if mask & selectors.EVENT_WRITE:  # if server is sending stuff
        if data.outb:
            # since we appended stuff to field data.outbound, we are now going to send it
            print("sending", str(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ: # if server is going to read data
        recv_data = sock.recv(1024).decode()  # Should be ready to read
        if recv_data:
            print("received", str(recv_data), "from connection", data.addr)
            # now we have received stuff and we append this to outbound data
            #data.outb += recv_data
            # look at recv_data - go to that function
            if recv_data == 'create_new_list()' and data.sent_msg == 1:
                data.set_name_fst = True
                get_list_name(key, mask)
            elif recv_data == 'create_new_list()':
                data.set_name = True
                get_list_name(key, mask)
            elif recv_data == 'm':
                data.outb = welcome.encode()
            elif recv_data == 'edit_list()':
                get_list_name(key, mask)
                data.edit=True
            elif recv_data == 'a':
                data.edit=False
                data.add=True
                send_list(key, mask)
            elif recv_data == 'd':
                # we are deleting items from a list
                data.delete=True
                send_list(key, mask)
            elif recv_data == 'show_list()':
                data.delete=False
                data.add=False
                send_list(key, mask)
            elif recv_data == 'show_lists()':
                # now we want to send to client a dictionary of all lists that he/she is subscribing to
                data.show=True
                get_lists(key, mask)
            else:
                # at this stage, we are receiving list data
                handle_list_data(recv_data, key, mask)
        else:   # if we did not receive data from client - then close connection
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:    # if server is sending stuff
        if data.outb:
            data.sent_msg += 1
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

