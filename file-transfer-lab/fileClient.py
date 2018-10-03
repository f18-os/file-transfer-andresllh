#! /usr/bin/env python3
'''
Your assignment is to write fileClient.py and fileServer.py which can transfer a file ("put") from a client to the server. Your programs should:

be in the file-transfer-lab subdir
work with and without the proxy
support multiple clients simultaneously using fork()
gracefully deal with scenarios such as:
zero length files
user attempts to transmit a file which does not exist
file already exists on the server
the client or server unexpectedly disconnect
optional (unless you're taking this course for grad credit): be able to request ("get") files from server
'''


import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)
   
   

user_input = input('What file would you like to send?')
try:
    f = open(user_input, 'r')
except:
    print('Error while opening file, make sure that it exists and is in the current directory')
        
print('Sending file to server')
lines = f.readlines()
framedSend(s, bytearray(user_input.strip('\n'), 'utf-8'), debug)
for line in lines:
# need to encode line as bytes
    if line is '\n':
        line = ' ' + line
    line = bytearray(line.strip('\n'), 'utf-8')
    framedSend(s, line, debug)
try:
    print("received:", framedReceive(s, debug))
except:
    print('Error while receiving')
            

