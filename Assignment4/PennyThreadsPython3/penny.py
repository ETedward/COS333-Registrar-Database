#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv, stderr
from threading import Thread
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM
from pickle import load, dump
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout
from PyQt5.QtWidgets import QTextEdit

#-----------------------------------------------------------------------

class WorkerThread (Thread):

    def __init__(self, host, port, author, booksTextEdit):
        Thread.__init__(self)
        self._host = host
        self._port = port
        self._author = author 
        self._booksTextEdit = booksTextEdit
        
    def run(self):        
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self._host, self._port))
        
        outFlo = sock.makefile(mode='wb')
        dump(self._author, outFlo)
        outFlo.flush()
    
        inFlo = sock.makefile(mode='rb')
        books = load(inFlo)
        sock.close()
    
        # Run-time error:
        self._booksTextEdit.clear()
        if len(books) == 0:
            self._booksTextEdit.insertPlainText('(None)')
        for book in books:
            self._booksTextEdit.insertPlainText(str(book) + '\n')
        self._booksTextEdit.repaint()
            
#-----------------------------------------------------------------------

def main():

    if len(argv) != 3:
        print('Usage: penny host port', file=stderr)
        return
    try:
        host = argv[1]
        port = int(argv[2])
    except Exception as e:
        print(e, file=stderr)
        return

    # Create and lay out the widgets.
    
    app = QApplication([])

    authorLabel = QLabel('Author: ')
    authorLineEdit = QLineEdit()
    booksTextEdit = QTextEdit()
    booksTextEdit.setReadOnly(True)
    
    layout = QGridLayout()
    layout.addWidget(authorLabel, 0, 0)
    layout.addWidget(authorLineEdit, 0, 1)
    layout.addWidget(booksTextEdit, 1, 0, 1, 2)
    layout.setRowStretch(0, 0)
    layout.setRowStretch(1, 1)
    layout.setColumnStretch(0, 0)
    layout.setColumnStretch(1, 1)
    layout.setColumnStretch(2, 0)

    frame = QFrame()
    frame.setLayout(layout)
    
    window = QMainWindow()
    window.setWindowTitle('Penny: Author Search')
    window.setCentralWidget(frame)
    screenSize = QDesktopWidget().screenGeometry()
    window.resize(screenSize.width()//2, screenSize.height()//2)

    # Handle signals.

    def authorSlot():    
        author = authorLineEdit.text()
        workerThread = WorkerThread(host, port, author, booksTextEdit)
        workerThread.start()

    authorLineEdit.textChanged.connect(authorSlot)
 
    authorSlot()  # Populate booksTextEdit initially.
    
    # Show the window and start the event loop.
    
    window.show()
    exit(app.exec_()) 

if __name__ == '__main__':
    main()