# Python TCP Client B
import socket

host = '127.0.0.1'
port = 2004
BUFFER_SIZE = 2000
MESSAGE = input("tcpClientB: Enter message/ Enter exit:")

tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientB.connect((host, port))

while MESSAGE != 'exit':
    tcpClientB.send(MESSAGE.encode())
    data = tcpClientB.recv(BUFFER_SIZE).decode()
    print(" Client received data:", data)
    MESSAGE = input("tcpClientB: Enter message to continue/ Enter exit:")

tcpClientB.close()