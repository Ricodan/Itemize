#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 65432

#tihs is a server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    # accept() creates a new socket. This is important since it's not the same as
    # the s object. addr is address for the Client that connects to us.

    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)