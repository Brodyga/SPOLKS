import socket
import threading
import sys

class Server(threading.Thread):
    def __init__(self, s):
        self.s = s
        threading.Thread.__init__(self)
    def run (self):
        write_mode, address = self.s.recvfrom(3)
        print 'Connection address:', address
        length, address = self.s.recvfrom(1)
        length = ord(length)
        file_name, address = self.s.recvfrom(length)
        file = open(file_name, 'ab')
        if write_mode == 'beg':
            file = open(file_name, "wb")
        elif write_mode == 'add':
            file = open(file_name, "ab")

        while True:
            try:
                data, address = self.s.recvfrom(BUFFER_SIZE)
                self.s.sendto('1', address)
                if not data:
                    break
                file.write(data)
            except Exception:
                file.close()
                print 'File Error'
                return
        print 'Address disconnected', address
        file.close()
        self.s.close()

UDP_IP = '127.0.0.1'
UDP_PORT = 2000
BUFFER_SIZE = 100

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

s.bind((UDP_IP, UDP_PORT))
#s.listen(1)

Server(s).start()
