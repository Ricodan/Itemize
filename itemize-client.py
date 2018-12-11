import socket
import multi_thread
import queue

HOST = '127.0.0.1'
PORT = 2004
BUFFER_SIZE = 1024
threads = []
client_queue = queue.Queue(10)

def print_confirm():
    print('Created new active socket')

def print_confirm_passive()
    print('Passive thread working')

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((HOST, PORT))

newThread = multi_thread.activeSocket(tcpClientA.getsockname()[1], client_queue, print_confirm())
newPassiveThread = multi_thread.passiveSocket(tcpClientA.getsockname()[1]+1,client_queue, print_confirm_passive())

