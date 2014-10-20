#!/usr/bin/env python
#OOB
import socket
import threading

class Server(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        threading.Thread.__init__(self)
    def run (self):
        print 'Connection address:', self.addr
        length = ord(self.conn.recv(1))
        file_name = self.conn.recv(length)
        file = open(file_name, "wb")
        while True:
            try:
                data = self.conn.recv(BUFFER_SIZE)
            except Exception:
                file.close()
                print 'Lost Connection'
                return
            if not data:
                break

            try:
                file.write(data)
            except Exception:
                file.close()
                print 'File Error'
                return
        print 'Address disconnected', self.addr
        file.close()
        self.conn.close()

TCP_IP = '192.168.43.195'#'192.168.1.157'#'127.0.0.1'
TCP_PORT = 2033
BUFFER_SIZE = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
while True:
    conn, addr = s.accept()
    Server(conn, addr).start()
    #Server(conn, addr).run()