#!/usr/bin/env python
import socket
import errno
import datetime
import time
import os
import struct
import sys

rst = 0
flag = 0
MESS_len = 0
BUFFER_SIZE = 50

class Client():
    def __init__(self, s):
        self.s = s

    def send_file_len(self, length_encode):
        global rst
        global flag
        flag = 0
        while flag == 0:
            try:
                if rst == 0:
                    self.s.sendto('beg', (UDP_IP, UDP_PORT))
                self.s.sendto(str(length_encode), (UDP_IP, UDP_PORT))
                flag = 1
            except socket.timeout:
                self.s.close()
                return
            except socket.error, err:
                if err[0] == errno.EWOULDBLOCK:
                    self.s.close()
                    return
                if err[0] == errno.EPIPE:
                    flag = 0
                    rst = 1
        return

    def send_file_name(self, length_encode, file_name):
        global rst
        global flag
        flag = 0
        while flag == 0:
            try:
                if rst == 1:
                    self.s.sendto('add', (UDP_IP, UDP_PORT))
                    self.send_file_len(length_encode)
                    rst = 0
                self.s.sendto(file_name, (UDP_IP, UDP_PORT))
                flag = 1
            except socket.timeout:
                self.s.close()
                return
            except socket.error, err:
                if err[0] == errno.EWOULDBLOCK:
                    self.s.close()
                    return
                if err[0] == errno.EPIPE:
                    flag = 0
                    try:
                        #self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        self.send_file_len(length_encode)
                        # Client(s).run()
                        #return
                    except socket.timeout:
                        self.s.close()
                        return
                    except Exception:
                        flag = 0
        return

    def send_file_data(self, length_encode, file_name, data):
        global rst
        global flag
        flag = 0
        while flag == 0:
            try:
                self.s.settimeout(5.0)
                self.s.sendto(data, (UDP_IP, UDP_PORT))
                data, address = self.s.recvfrom(1)
                if data != '1':
                    flag = 0
                flag = 1
            except socket.timeout:
                try:
                    print 'Check'
                    rst = 1
                    #self.s.settimeout(1.0)
                    self.send_file_name(length_encode, file_name)
                    self.s.sendto(data, (UDP_IP, UDP_PORT))
                    data, address = self.s.recvfrom(1)
                    if data != '1':
                        flag = 0
                except socket.timeout:
                    self.s.close()
                    print 'Timeout is gone'
                    return -1

            except socket.error, err:
                if err[0] == errno.EWOULDBLOCK:
                    self.s.close()
                    return
                if err[0] == errno.EPIPE or err[0] == errno.EBADF:
                    flag = 0
                    rst = 1
                    try:
                        #self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                        self.send_file_name(length_encode, file_name)
                        # Client(s).run()
                        #return
                    except socket.timeout:
                        self.s.close()
                        return
                    except Exception:
                        flag = 0

        return

    def run(self):
        global flag
        global MESS_len
        file_name = 'Daft Punk - The Son of Flynn.mp3'#'labs.pdf'#'Meat Loaf - Everything Louder Than Everyth else (clean version).mp3'
        try:
            file = open(file_name, "rb")
        except Exception:
            print 'File Not Found'
            return
        length_encode = chr(len(file_name))

        self.send_file_len(length_encode)
        self.send_file_name(length_encode, file_name)

        i = 1
        MESS_len = 0
        filesize = os.stat(file_name).st_size
        global BUFFER_SIZE
        while True:
            if flag == 0:
                return
            try:
                MESSAGE = file.read(BUFFER_SIZE)
                MESS_len += len(MESSAGE)
            except Exception:
                file.close()
                print 'File Error'
                self.s.close()
                return
            if len(MESSAGE) == 0:
                print 'File end'
                self.s.sendto('', (UDP_IP, UDP_PORT))
                break
            check = self.send_file_data(length_encode, file_name, MESSAGE)
            if check == -1:
                break
            if MESS_len >= filesize / 10 * i:
                print '' + str(10 * i) + '%'
                i += 1
        file.close()
        self.s.close()
        return


UDP_IP = '127.0.0.1'  # '192.168.43.195'
UDP_PORT = 2000
BUFFER_SIZE = 50

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(10.0)
Client(s).run()
