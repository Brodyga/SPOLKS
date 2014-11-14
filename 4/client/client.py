import socket
import errno
import datetime
import time
import os
import struct

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
        begin = time.time()
        while flag == 0:
            try:
                if rst == 0:
                    self.s.send('beg')
                self.s.send(str(length_encode))
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
                    if (time.time() - begin) > 10 and flag == 0:
                        flag = 0
                        flag1 = 1
                        self.s.close()
                        return
                    try:
                        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.s.connect((TCP_IP, TCP_PORT))
                        timeval = struct.pack('ll', 5, 0)
                        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)
                    except socket.timeout:
                        self.s.close()
                        return
                    except Exception:
                        flag = 0
        return

    def send_file_name(self, length_encode, file_name):
        global rst
        global flag
        flag = 0
        begin = time.time()
        while flag == 0:
            try:
                if rst == 1:
                    self.s.send('add')
                    self.send_file_len(length_encode)
                    rst = 0
                self.s.send(file_name)
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
                    if (time.time() - begin) > 10 and flag == 0:
                        flag = 0
                        flag1 = 1
                        self.s.close()
                        return
                    try:
                        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.s.connect((TCP_IP, TCP_PORT))
                        timeval = struct.pack('ll', 5, 0)
                        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)
                        self.send_file_len(length_encode)
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
        begin = time.time()
        while flag == 0:
            if (time.time() - begin) > 10 and flag == 0:
                flag = 0
                file.close()
                self.s.close()
                return
            try:
                self.s.settimeout(5.0)
                self.s.send(data)
                flag = 1
            except socket.timeout:
                self.s.close()
                return

            except socket.error, err:
                if err[0] == errno.EWOULDBLOCK:
                    self.s.close()
                    return
                if err[0] == errno.EPIPE or err[0] == errno.EBADF:
                    flag = 0
                    rst = 1
                    if (time.time() - begin) > 10 and flag == 0:
                        flag = 0
                        flag1 = 1
                        self.s.close()
                        return
                    try:
                        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.s.connect((TCP_IP, TCP_PORT))

                        timeval = struct.pack('ll', 5, 0)
                        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)

                        self.send_file_name(length_encode, file_name)
                    except socket.timeout:
                        self.s.close()
                        return
                    except Exception:
                        flag = 0

        return

    def run(self):
        global flag
        global MESS_len
        file_name = 'file_name'
        try:
            file = open(file_name, "rb")
        except Exception:
            print 'File Not Found'
            return
        length_encode = chr(len(file_name))
        timeval = struct.pack('ll', 5, 0)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)

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
                break
            self.send_file_data(length_encode, file_name, MESSAGE)
            if MESS_len >= filesize / 10 * i:
                enc = chr(10 * i)
                self.s.send(str(enc), socket.MSG_OOB)
                i += 1
        file.close()
        self.s.close()
        return


TCP_IP = '127.0.0.1'
TCP_PORT = 2000
BUFFER_SIZE = 50

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5.0)
try:
    s.connect((TCP_IP, TCP_PORT))
except Exception:
    print 'Wrong IP'
else:
    Client(s).run()
