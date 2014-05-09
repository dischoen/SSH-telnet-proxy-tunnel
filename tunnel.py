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
#
# available from github.com/dischoen/SSH-telnet-proxy-tunnel.git
#
import sys
import socket
import os
import time
import select
import fcntl

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
    for fd in r:
        if fd == s:
            data = s.recv(4096)
            for line in data.split('\n'):
                if line.find("Connected") == 0:
                    true = False
                    continue
                if true != True:
                    sys.stdout.write(line)
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    break

true = True
while true:
    (r,w,x) = select.select([sys.stdin,s],[],[])
    for fd in r:
        if fd == s:
            data = s.recv(4096)
            if not data:
                true = False
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        if fd == sys.stdin:
            data = sys.stdin.read(4096)
            if not data:
                true = False
                break
            s.send(data)
