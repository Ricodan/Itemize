import socket
import queue
import server_worker
import multi_thread
import threading

class server_worker(threading.Thread):
    def __init__(self, port, queue, function):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.function = function


    def run(self):
            # depending on the output you put something on the queeu or you don't
            self.function(self.port)

HOST = '127.0.0.1'
TCP_PORT = 2004
BUFFER_SIZE = 1024

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((HOST,TCP_PORT))
threads = []
server_comm_queue = queue.Queue(10)
active_thread_queue = queue.Queue(10)
passive_thread_queue = queue.Queue(10)

# def hello_active(queue):
#     print('Created active server socket')
#     # check if active server socket can write to passive client socket
#     msg = 'now active server socket is talking to passive client socket'
#     data =

def hello_passive(queue):
    print('Created passive server socket')
    # check if passive server socket can read out msgs from active client socket
    msg = queue.get()
    print(msg)

def create_active_passive(sock, port, active_queue, passive_queue):
    print("Now we are trying to create the two sockets at server worker node")
    active_thread = multi_thread.activeSocket(port+1, passive_queue)
    passive_thread = multi_thread.passiveSocket(sock, port, active_queue)
    active_thread.start()
    passive_thread.start()
    threads.append(active_thread)
    threads.append(passive_thread)

while True:
    print( "Now we listen")
    tcpServer.listen(4)

    (conn, (ip, port)) = tcpServer.accept()
    # we create a new server worker thread with an import function
    newThread = multi_thread.server_worker(conn, port, server_comm_queue, active_thread_queue, passive_thread_queue, create_active_passive)
    print('created new thread in server')
    newThread.start()
    threads.append(newThread)
    server_comm_queue.put('now i talk to server worker')
    # get msg from server worker
    print('A')
    #msg = server_comm_queue.get()
    print('B')
    #print(msg)

for t in threads:
        t.join()