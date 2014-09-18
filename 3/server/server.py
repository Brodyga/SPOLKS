import socket
import threading

class Server(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        threading.Thread.__init__(self)
    def run (self):
        print 'Connection address:', self.addr
        file = open('/home/brodyga/temp.c', "wb")
        while True:
            data = self.conn.recv(BUFFER_SIZE)
            if not data:
                break
            file.write(data)
        print 'Address disconnected', self.addr
        file.close()
        self.conn.close()

TCP_IP = '127.0.0.1'
TCP_PORT = 2010
BUFFER_SIZE = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
while True:
    conn, addr = s.accept()
    Server(conn, addr).start()