import socket
import multi_thread
import queue
import sys
import multi_thread as mt


import types
import client_service_conn


HOST = '127.0.0.1'
PORT = 2004
BUFFER_SIZE = 1024
threads = []
client_ID = int(sys.argv[1])

def dummy_func(sock, queue):
    sock.accept()
    print("shit works")
    #sleep(1000)

a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
b.bind((HOST, 6000+client_ID))
a.connect((HOST, PORT)) # change this to the sockets host and port
mt.node(b,0,None, dummy_func).start()


while True:
    input("Yoyoo waddup")

for t in threads:
        t.join()
