#!/usr/bin/env python
import socket
import datetime
import time

flag1 = 0

class Client():
    def __init__(self, s):
        self.s = s
    def run(self):
        global flag1
        file_name = 'file.txt'
        try:
            file = open(file_name, "rb")
        except Exception:
            print 'File Not Found'
            return
        length_encode = chr(len(file_name))
        flag = 0
        begin = time.time()
        while flag == 0:
            try:
                self.s.send(str(length_encode))
                flag = 1
            except Exception:
                flag = 0

                if (time.time() - begin) > 2 and flag == 0:
                    flag1 = 1
                    self.s.close()
                    return
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((TCP_IP, TCP_PORT))
                    Client(s).run()
                    return
                except Exception:
                    flag = 0
                    if flag1 == 1:
                        return


        flag = 0
        begin = time.time()
        while flag == 0:
            try:
                self.s.send(file_name)
                flag = 1
            except Exception:
                #file.close()
                if (time.time() - begin) > 2 and flag == 0:
                    flag1 = 1
                    self.s.close()
                    return
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((TCP_IP, TCP_PORT))
                    Client(s).run()
                    flag1 = 1
                    return
                except Exception:
                    flag = 0
                    if flag1 == 1:
                        return
                #print 'Lost Connection'
                #return

        while True:
            try:
                MESSAGE = file.read(BUFFER_SIZE)
            except Exception:
                file.close()
                print 'File Error'
                return
                file.close()
            if len(MESSAGE) == 0:
                break

            flag = 0
            begin = time.time()
            while flag == 0:
                if (time.time() - begin) > 2 and flag == 0:
                    flag1 = 1
                    file.close()
                    self.s.close()
                    return
                try:
                    self.s.send(MESSAGE)
                    flag = 1
                except Exception:
                    flag = 0
                    #file.close()
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((TCP_IP, TCP_PORT))
                        Client(s).run()
                        return
                    except Exception:
                        flag = 0
                        if flag1 == 1:
                            return
                    #print 'Lost Connection'
                    #return
        flag1 = 1
        file.close()
        self.s.close()

TCP_IP = '192.168.43.195'#'192.168.43.195'
TCP_PORT = 2033
BUFFER_SIZE = 50

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((TCP_IP, TCP_PORT))
    s.setsockopt(socket.SOL_SOCKET, )
except Exception:
    print 'Wrong IP'
else:
    Client(s).run()
