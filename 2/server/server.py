import socket
from multiprocessing.dummy import Pool as ThreadPool

def Serv(arg):
    s.listen(1)
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        conn.send(data)
    print 'Address disconnect', addr
    conn.close()


TCP_IP = '127.0.0.1'
TCP_PORT = 2000
BUFFER_SIZE = 5

pool = ThreadPool(16)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
arg = [0] * 16
pool.map(Serv, arg)

pool.close()
pool.join()