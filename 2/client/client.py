#!/usr/bin/env python

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

amount_received = 0

while(1):
    MESSAGE = raw_input('sent data:')
    amount_sended = len(MESSAGE)
    s.send(MESSAGE)

    data_res = ''
    while amount_received < amount_sended:
        data = s.recv(BUFFER_SIZE)
        amount_received += len(data)
        data_res += data
        #if not data: break
        if data_res == 'exit':
            break

    if data_res == 'exit': break
    print 'received data:', data_res
    amount_received = 0
s.close()