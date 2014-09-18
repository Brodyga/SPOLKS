import socket

class Client():
    def __init__(self, s):
        self.s = s
    def run(self):
        file = open('/home/brodyga/main.c', "rb")
        while True:
            MESSAGE = file.read(20)
            if len(MESSAGE) == 0:
                break
            s.send(MESSAGE)
        file.close()
        s.close()



TCP_IP = '127.0.0.1'
TCP_PORT = 2010
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
Client(s).run()