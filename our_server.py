#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 65432

list_1 = ['apple', 'bananas']

def checkData(data, sock):
    global list_1
    # match msg against different commands
    print('2')
    if data == b'showLists':
        sock.sendall(bytes(list_1))



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # associate socket with addr and port nr
    s.listen() # listen for connections
    conn, addr = s.accept() # conn is new socket connecting server to new client, addr is address of client
    with conn:
        print('Connected by ', addr)
        while True:
            data = conn.recv(1024) #receive dat
            print('1')
            checkData(data, conn)
            if not data:
                break
            conn.sendall(data) # send back data to client

