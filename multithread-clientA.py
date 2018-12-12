import socket
from threading import Thread
from socketserver import ThreadingMixIn

class ClientListener(Thread):

    def __init__(self, socket, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.queue = []
        print('[+] New client listener socket started for ', ip, ":", str(port))

    def run(self):
        while True:
            data = tcpClientListen.recv(1024).decode()
            print('Client listener received data: ', data)
            MESSAGE = input("Multithreaded Python client : Enter Response from client/Enter exit:")
            if MESSAGE == 'exit':
                break
            tcpClientListen.send(MESSAGE.encode())  # echo

host = '127.0.0.1'
port = 2004
BUFFER_SIZE = 1024
threads = []
MESSAGE = input("tcpClientA: Enter message/ Enter exit:")

# create the listening socket first
tcpClientListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientListen.connect((host, port))
# now we make a new thread for this listening socket
listeningThread = ClientListener(tcpClientListen, host, tcpClientListen.getsockname()[1] )
listeningThread.start()
print('starting new listener thread')
threads.append(listeningThread)

# now we are in main thread and we create the principal socket

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))
print('we have created the principal socket')

while MESSAGE != 'exit':
    tcpClientA.send(MESSAGE.encode())
    data = tcpClientA.recv(BUFFER_SIZE).decode()
    print(" Client2 received data:", data)
    MESSAGE = input("tcpClientA: Enter message to continue/ Enter exit:")

tcpClientA.close()

for t in threads:
    t.join()