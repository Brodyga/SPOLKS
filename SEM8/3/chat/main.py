import socket
import threading
import sys

exit_flag = False
ip_list = []


class Receiver(threading.Thread):
    def __init__(self, s):
        self.s = s
        threading.Thread.__init__(self)
        #self.ip_list = []
    def run(self):
        flag = False
        global ip_list
        global exit_flag
        while True:
            data, addr = self.s.recvfrom(1024)
            if data == 'init':
                if flag == False:
                    flag = True
                    print 'Welcome to chatroom user - %s' % (addr[0])
                    ip_list.append(addr[0])
                else:
                    if addr[0] not in ip_list:
                        print 'New user enter in chatroom - %s' % (addr[0])
                        ip_list.append(addr[0])

            elif data == 'exit':
                if exit_flag == True:
                    return
                print 'User %s leave the chatroom' % (addr[0])
                ip_list.remove(addr[0])
            else:
                if addr[0] not in ip_list:
                        print 'New user enter in chatroom - %s' % (addr[0])
                        ip_list.append(addr[0])

                if addr[0] != ip_list[0]:
                    print '%s: %s' % (addr[0], data)

            if exit_flag == True:
                return

        #self.s.close()


class Sender(threading.Thread):
    def __init__(self, s):
        self.s = s
        threading.Thread.__init__(self)

    def run(self):
        #self.s.sendto('init', ('192.168.0.255', 2000))
        self.s.sendto('init', ('<broadcast>', 2000))
        global ip_list
        while True:
            msg = raw_input()
            if msg == 'ls':
                for a in ip_list:
                    print '%s' % (a)
            else:
                #self.s.sendto(msg, ('192.168.0.255', 2000))
                self.s.sendto(msg, ('<broadcast>', 2000))
                if msg == 'exit':
                    global exit_flag
                    exit_flag = True
                    print 'Good Bye'
                    self.s.close()
                    return
                    break
        self.s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

s.bind(('', 2000))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

Receiver(s).start()
Sender(s).start()