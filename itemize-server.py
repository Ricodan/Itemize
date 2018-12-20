import socket
import queue
import server_worker
import multi_thread
import threading
#TODO:
# - The code works for ONE server_worker.
# - Make it so it works for many! 
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
client_dict = {}
client_ID = 0


# these functions run by server workers
def notify_client(sock, queue):
    print("Waiting for notification for client. \n")
    msg = queue.get().encode()
    print(str(msg))
    #sock.send(queue.get().encode())
    sock.send(msg)
    
def notify_server(sock, queue):
    print("Waiting for notification for client message. \n")
    msg = sock.recv().decode()
    #queue.put(sock.recv().decode())
    queue.put(msg)

# this queue goes from sw to server
notification_queue = queue.Queue(10)

while True:

    print( "Now we listen")
    tcpServer.listen(4)

    (sock, (ip, port)) = tcpServer.accept()
    print(str(sock))
    server_comm_queue = queue.Queue(10)

    # here we create a dictionary mapping clientID's to subscriptions
    client_ID += 1
    client_dict[client_ID] = server_comm_queue

    a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a.connect(('localhost', 6000+client_ID)) # change this to the sockets host and port
    
    # we create a new server worker thread with an import function
    newThread = multi_thread.server_worker(multi_thread.node(sock,port,server_comm_queue, notify_server), multi_thread.node(a,port+1, notification_queue, notify_client))
    print('created new thread server worker in server')
    newThread.start()
    threads.append(newThread)

for t in threads:
        t.join()
