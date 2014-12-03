import socket
import threading
import sys
import select

UDP_IP = '127.0.0.1'
UDP_PORT = 2000
BUFFER_SIZE = 100

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

s.bind((UDP_IP, UDP_PORT))

inputs = []

file_mas = []

while 1:

    read_sockets, write_sockets, error_sockets = select.select([s], [], [])

    for sock in read_sockets:

        #New connection
        if sock is s:

            write_mode, address = sock.recvfrom(BUFFER_SIZE)#3)
            if not (address in inputs):
                print 'Connection address:', address
                length, address = sock.recvfrom(1)
                length = ord(length)
                file_name, address = sock.recvfrom(length)
                #file = open(file_name, 'ab')
                if write_mode == 'beg':
                    file = open(file_name, "wb")
                elif write_mode == 'add':
                    file = open(file_name, "ab")

                inputs.append(address)
                file_mas.append(file)

            else:
                try:
                    data = write_mode
                    sock.sendto('1', address)
                    if not data:
                        print 'Address disconnected', address
                        #sock.close()
                        file_mas[inputs.index(address)].close()
                        file_mas.remove(file_mas[inputs.index(address)])
                        inputs.remove(address)
                        continue
                    else:
                        ind = inputs.index(address)
                        file = file_mas[ind]
                        file.write(data)
                except Exception:
                    ind = inputs.index(address)
                    file_mas[ind].close()
                    print 'File Error'
                    break

s.close()