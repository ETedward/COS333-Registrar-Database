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
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QTimer

workerThread = None

#-----------------------------------------------------------------------

class WorkerThread (Thread):

    def __init__(self, host, port, author, queue):
        Thread.__init__(self)
        self._host = host
        self._port = port
        self._author = author 
        self._queue = queue
        self._shouldStop = False
    
    def stop(self):
        self._shouldStop = True
        
    def run(self):        
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self._host, self._port))
        
        outFlo = sock.makefile(mode='wb')
        dump(self._author, outFlo)
        outFlo.flush()
    
        inFlo = sock.makefile(mode='rb')
        books = load(inFlo)
        sock.close()
        
        if self._shouldStop:
            return

        self._queue.put(books)

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

    queue = Queue()
    
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
        global workerThread
        author = authorLineEdit.text()
        if workerThread is not None:
            workerThread.stop()
        workerThread = WorkerThread(host, port, author, queue)
        workerThread.start()
    
    authorLineEdit.textChanged.connect(authorSlot)

    authorSlot()  # Populate booksText initially.
    
    # Create a timer that polls the queue.

    def pollQueue():
        while not queue.empty():
            books = queue.get()           
            booksTextEdit.clear()
            if len(books) == 0:
                booksTextEdit.insertPlainText('(None)')
            for book in books:
                booksTextEdit.insertPlainText(str(book) + '\n')
            booksTextEdit.repaint()

    timer = QTimer()
    timer.timeout.connect(pollQueue)
    timer.start()  
    
    # Show the window and start the event loop.
    
    window.show()
    exit(app.exec_()) 

if __name__ == '__main__':
    main()
