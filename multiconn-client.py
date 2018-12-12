#!/usr/bin/env python3

import threading
import sys
import socket
import selectors
import types
import json



sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]





def start_connections(host, port, num_conns):
    server_addr = (host, port)

    for i in range(0, num_conns):
        connid = i + 1
        print("starting connection", connid, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2  = sock.dup

        sock2.setblocking(False)
        sock.setblocking(False)

        sock2.connect_ex(server_addr)
        sock.connect_ex(server_addr)


        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            sent_msgs=0,
            messages=list(messages),
            outb=b"",
            add=False,
            delete=False,
            list=None,
            cont=False,
            show=False,
            show_all=False
        )
        sel.register(sock, events, data=data)

def enter_list_name(key, mask):
    # read user input
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_WRITE:
        if not data.outb:
            # read from user input
            data.outb = input("Enter name of list\n")
            data.list = data.outb
            # nu innhåller data.outb något så då skickar vi på socketen
        if data.outb:
            print("sending", str(data.outb), "to connection", data.connid)
            sent = sock.send(data.outb.encode())  # Should be ready to write
            data.outb = data.outb[sent:]

def print_list(list):
    i=1
    for item in list:
        print(i, '.\t', item)
        i+=1

def get_list(key, mask):
    sock = key.fileobj
    data = key.data
    data.outb = 'show_list()'
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("sending", str(data.outb), "to connection", data.connid)
            sent = sock.send(data.outb.encode())  # Should be ready to write
            data.sent_msgs += 1
            data.outb = data.outb[sent:]
            data.show=True

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        print('we are reading')
        print(data.show_all)
        if data.show:
            # receive json
            recv_data = sock.recv(1024)
            recv_data = json.loads(recv_data)
            print('Items in list ', data.list, ': \n')
            print_list(recv_data[data.list])
            data.show=False
            data.outb = input('Your input: ')
        elif data.show_all:
            recv_data = sock.recv(1024)
            recv_data = json.loads(recv_data)
            print('These are your lists:\n')
            print_list(recv_data)
            data.show_all = False
            data.show=True
            # get input from user
            data.outb = input('Type index of list to display: ')
            index = int(data.outb)-1
            data.list = recv_data[index]
            if mask & selectors.EVENT_WRITE:
                if data.outb:
                    print("sending", str(data.outb), "to connection", data.connid)
                    sent = sock.send(data.outb.encode())  # Should be ready to write
                    data.sent_msgs += 1
                    data.outb = data.outb[sent:]
        elif data.add:
            # receive json
            recv_data = sock.recv(1024)
            recv_data = json.loads(recv_data)
            print('Items in list ', data.list, ': \n')
            print_list(recv_data[data.list])
            data.add=False
            # get input from user
            while data.cont:
                data.outb = input('Item to add: ')
                if mask & selectors.EVENT_WRITE:
                    if data.outb:
                        print("sending", str(data.outb), "to connection", data.connid)
                        sent = sock.send(data.outb.encode())  # Should be ready to write
                        data.sent_msgs += 1
                        data.outb = data.outb[sent:]
                answer = input('Add another item? (Y/N) ')
                if answer == 'N' or answer == 'n':
                    data.cont = False
            # now we want to get the finished list from server
            get_list(key, mask)
        elif data.delete:
            # receive json
            recv_data = sock.recv(1024)
            recv_data = json.loads(recv_data)
            print('Items in list ', data.list, ': \n')
            print_list(recv_data[data.list])
            data.delete = False
            # get input from user
            while data.cont:
                data.outb = input('Enter number of item to delete: ')
                if mask & selectors.EVENT_WRITE:
                    if data.outb:
                        print("sending", str(data.outb), "to connection", data.connid)
                        sent = sock.send(data.outb.encode())  # Should be ready to write
                        data.sent_msgs += 1
                        data.outb = data.outb[sent:]
                answer = input('Delete another item? (Y/N) ')
                if answer == 'N' or answer == 'n':
                    data.cont = False
            # now we want to get the finished list from server
            get_list(key, mask)

        else:
            recv_data = sock.recv(1024).decode()  # Should be ready to read
            if recv_data:
                data.recv_total += 1
                print("received", str(recv_data), "from connection", data.connid)
                if recv_data == 'Enter name of list: ':
                    # go to function enter_list_name
                    enter_list_name(key, mask)
                elif recv_data == "Press 'a' to add items to list\nPress 'd' to delete items from list":
                    # now we will send a character to server and receive json object back
                    data.outb = input('Your input: ')
                    if data.outb == 'a':
                        data.cont=True
                        data.add=True
                    else:
                        data.cont=True
                        data.delete=True
                elif not data.recv_total == 1 and not data.sent_msgs == 0:
                    # if we want input from user
                    data.outb = input('Your input: ')
                    if data.outb == 'show_lists()':
                        data.show_all=True
                        print('setting data.show_all to ', data.show_all)
        if not recv_data or data.recv_total == data.msg_total:
            print("closing connection", data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.recv_total == 1 and data.sent_msgs == 0:
            # read from user input
            data.outb = input("Enter your function\n")
            # nu innhåller data.outb något så då skickar vi på socketen
        #if not data.outb:
            # read from user input
            #data.outb = input("Enter your function\n")
            # nu innehåller data.outb något så då skickar vi på socketen
        if data.outb:
            print("sending", str(data.outb), "to connection", data.connid)
            sent = sock.send(data.outb.encode())  # Should be ready to write
            data.sent_msgs += 1
            data.outb = data.outb[sent:]


if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

host, port, num_conns = sys.argv[1:4]
start_connections(host, int(port), int(num_conns))

#one thread will have one port and the other thread will have another port


listening_thread = eventThread(1, "listening", host, port+1, sel)


try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()








#Create nodes with 2 sockets that is always listening and the other is sending commands to the server.
#"since sock.recv is blocking then it's better to sue threads, like 2 threads, or asyncIO. when there's something
#in the queue then execute it

#Create two threads, one with recv thread and the other with keyboard input
