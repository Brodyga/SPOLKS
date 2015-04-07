#!/usr/bin/env python
import os
import sys
import socket
import struct
import select
import time
import threading

ICMP_ECHO_REQUEST = 8
i = 0
flag = 0

source_ip = '0.0.0.0'
dest_ip = '255.255.255.255'

ip_ihl = 5
ip_ver = 4
ip_tos = 0
ip_tot_len = 0  # kernel will fill the correct total length
ip_id = 54321
ip_frag_off = 0
ip_ttl = 255
ip_proto = socket.IPPROTO_ICMP
ip_check = 0    # kernel will fill the correct checksum
ip_saddr = socket.inet_aton(source_ip)
ip_daddr = socket.inet_aton(dest_ip)

ip_ihl_ver = (ip_ver << 4) + ip_ihl

# the ! in the pack format string means network order
ip_header = struct.pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

def checksum(source_string):
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count < countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum += thisVal
        sum &= 0xffffffff

        count += 2

    if countTo < len(source_string):
        sum += ord(source_string[len(source_string) - 1])
        sum &= 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum += sum >> 16

    answer = ~sum
    answer &= 0xffff

    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receive_one_ping(my_socket, ID, timeout):
    timeLeft = timeout
    while True:
        startedSelect = time.clock()
        whatReady = select.select([my_socket], [], [], timeLeft)

        howLongInSelect = (time.clock() - startedSelect)

        if whatReady[0] == []:
            return

        timeReceived = time.clock()
        recPacket, addr = my_socket.recvfrom(1024, socket.MSG_PEEK)
        icmpHeader = recPacket[20:28]

        type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
        if packetID == ID:
            my_socket.recvfrom(1024)
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft -= howLongInSelect
        if timeLeft <= 0:
            return


def send_one_ping(my_socket, dest_addr, ID, num):
    global i
    if i < num:
        i += 1
    if i < num or i == num:
        t = threading.Timer(1.0, send_one_ping, (my_socket, dest_addr, ID, num))
        if i < num:
            t.start()
        if i == num:
            t.cancel()
    dest_addr = socket.gethostbyname(dest_addr)

    my_checksum = 0

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    bytes_in_double = struct.calcsize("d")
    data = (192 - bytes_in_double) * "Q"
    data = struct.pack("d", time.clock()) + data

    # pseudo header fields
    global ip_header
    my_checksum = checksum(header + data)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1)
    packet = ip_header + header + data
    try:
        my_socket.sendto(packet, (dest_addr, 1))
    except Exception, e:
        global flag
        if flag == 1 and i == num:
            return


def ping(dest_addr, timeout=2, count=3):
    icmp = socket.getprotobyname("icmp")
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        icmp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error, (errno, msg):
        if errno == 1:
            raise

    ID = os.getpid() & 0xFFFF
    send_one_ping(my_socket, dest_addr, ID, count)
    for i in xrange(count):
        print "ping %s..." % dest_addr,
        delay = receive_one_ping(icmp_socket, ID, timeout)
        if delay is None:
            print "failed. (timeout within %ssec.)" % timeout
        else:
            delay *= 1000
            print "get ping in %0.4fms" % delay
    global flag
    flag = 1
    my_socket.close()

if __name__ == '__main__':
    ping(dest_ip)