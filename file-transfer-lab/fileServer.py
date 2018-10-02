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

import sys, os, socket
sys.path.append("../lib")       # for params
import params



switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        f = open('received.txt', 'w+')
        while True:
            payload = framedReceive(sock, debug)
            rec = str(payload)
            rec = rec[2:-1]
            f.write(rec + '\n')
            if debug: print("rec'd: ", payload)
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)
            payload += b"!"             # make emphatic!
            framedSend(sock, payload, debug)
        f.close()

