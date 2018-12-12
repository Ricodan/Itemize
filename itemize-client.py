import socket
import multi_thread
import queue

HOST = '127.0.0.1'
PORT = 2004
BUFFER_SIZE = 1024
threads = []
active_queue = queue.Queue(10)
passive_queue = queue.Queue(10)

def print_confirm_passive(queue):
    print('Passive thread working')
    # check if passive client socket can read out msgs from active server socket
    data = new_passive_thread.recv(1024).decode()
    print(data)


tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((HOST, PORT))

# should we really create a new thread for the active client socket or should it rather run in the main thread??
#new_active_thread = multi_thread.activeSocket(tcpClientA.getsockname()[1], active_queue, print_confirm)
new_passive_thread = multi_thread.passiveSocket(tcpClientA.getsockname()[1]+1,passive_queue)
#new_active_thread.start()
new_passive_thread.start()
print('started passive thread')
#threads.append(new_active_thread)
threads.append(new_passive_thread)
msg = 'check if active client socket can communicate with passive server socket'
tcpClientA.send(msg.encode())

for t in threads:
        t.join()