import socket
import queue
import multi_thread

HOST = '127.0.0.1'
TCP_PORT = 2004
BUFFER_SIZE = 1024

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((HOST,TCP_PORT))
threads = []
comm_queue = queue.Queue(10)

def hello_world():
    print("Hello World")

while True:
    print( "Now we listen")
    tcpServer.listen(4)

    (conn, (ip, port)) = tcpServer.accept()
    newThread = multi_thread.serverWorker(port, comm_queue,hello_world())
