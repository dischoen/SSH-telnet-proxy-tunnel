#!/usr/bin/python

# tunnel.py
#
# Usage: tunnel.py telnet-proxy telnet-proxy-port destination-host destination-port
#
# ssh-tunnel over a telnet proxy.  
#
# Written for HTTP CONNECT by Urban Kaveus <urban@statt.ericsson.se>,
# modified by Simon Josefsson <simon@josefsson.org> June 2000.
#
# Converted to python/single process
# by Dieter Schoen <dieter@schoen.or.at> May 2014.

import sys
import socket
import os
import time
import select
import fcntl

log = open("./tunnel.log", "wb")

proxy       = sys.argv[1]
proxyport   = sys.argv[2]
destination = sys.argv[3]
destport    = sys.argv[4]

protocol = socket.getprotobyname("tcp")

fcntl.fcntl(sys.stdin,  fcntl.F_SETFL, os.O_NONBLOCK)
fcntl.fcntl(sys.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, protocol)
s.connect((proxy,int(proxyport)))
s.send("CONNECT %s %s\r\n" % (destination, destport))

true = True
while true:
    (r,w,x) = select.select([sys.stdin,s],[],[])
    #log.write("1 %s,%s,%s\n" %(r,w,x))
    for fd in r:
        if fd == s:
            data = s.recv(4096)
            log.write("\n:A<%d>:" % len(data))
            log.write(data)
            log.write("\n:E:")
            for line in data.split('\n'):
                log.write("\n:LINE:%s\n" % line)
                if line.find("Connected") == 0:
                    log.write("\n\nFound Connected\n\n")
                    true = False
                    continue
                if true != True:
                    log.write("\n:<==:%s\n" % line)
                    sys.stdout.write(line)
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    break

log.write("\n:NOW2:\n")

true = True
while true:
    (r,w,x) = select.select([sys.stdin,s],[],[])
    log.write("\n2 %s\n" % r)
    for fd in r:
        if fd == s:
            data = s.recv(4096)
            if not data:
                true = False
                break
            log.write("\n:sA<%d>:" % len(data))
            log.write(data)
            log.write("\n:sE:")
            sys.stdout.write(data)
            sys.stdout.flush()
        if fd == sys.stdin:
            log.write("\n:l@@:")
            data = sys.stdin.read(4096)
            log.write("\n:lA@@<%d>:" % len(data))
            log.write(data)
            log.write("\n:lE:")
            s.send(data)
