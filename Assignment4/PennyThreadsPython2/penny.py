#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv, stderr
from socket import socket, AF_INET, SOCK_STREAM
from pickle import load, dump
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout
from PyQt5.QtWidgets import QTextEdit

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

        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
        
        outFlo = sock.makefile(mode='wb')
        dump(author, outFlo)
        outFlo.flush()
                
        inFlo = sock.makefile(mode='rb')
        books = load(inFlo)                  
        sock.close()
                    
        booksTextEdit.clear()
        if len(books) == 0:
            booksTextEdit.insertPlainText('(None)')
        for book in books:
            booksTextEdit.insertPlainText(str(book) + '\n')
        booksTextEdit.repaint()
            
    authorLineEdit.textChanged.connect(authorSlot)
    
    authorSlot()  # Populate booksTextEdit initially.
    
    # Show the window and start the event loop.
    
    window.show()
    exit(app.exec_())         

if __name__ == '__main__':
    main()
