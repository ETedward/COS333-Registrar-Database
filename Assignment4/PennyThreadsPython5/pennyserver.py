#!/usr/bin/env python

#-----------------------------------------------------------------------
# pennyserver.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import exit, argv, stderr
from socket import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from pickle import load, dump
from time import sleep
from database import Database

#-----------------------------------------------------------------------

def handleClient(sock, delay):
    
    inFlo = sock.makefile(mode='rb')
    author = load(inFlo)   
    print('Received author: ' + author)      
    
    if author.strip() == '':
        books = []
    else:
        database = Database()
        database.connect()
        books = database.search(author)
        database.disconnect()
     
    # Sleep for delay seconds to simulate a slow server response.
    sleep(delay)
    
    outFlo = sock.makefile(mode='wb')
    dump(books, outFlo)
    outFlo.flush() 

#-----------------------------------------------------------------------

def main(argv):

    BACKLOG = 5

    if len(argv) != 3:
        print('Usage: python %s port delay' % argv[0])
        exit(1)

    try:
        port = int(argv[1])
        delay = int(argv[2])

        serverSock = socket(AF_INET, SOCK_STREAM)
        serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print('Opened server socket')
        serverSock.bind(('', port))
        print('Bound server socket to port')
        serverSock.listen(BACKLOG)
        print('Listening')
                
        while True:
            try:
                sock, address = serverSock.accept()
                print('Accepted connection, opened socket')
                
                handleClient(sock, delay) 
                
                sock.close()
                print('Closed socket')          
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
