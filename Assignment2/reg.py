#!/usr/bin/env python

# -----------------------------------------------------------------------
# reg.py
# Author: Edward and Bharat
# -----------------------------------------------------------------------


#import server/socket handling
from sys import exit, argv, stderr
from socket import socket, AF_INET, SOCK_STREAM
from pickle import load
from pickle import dump

#import GUI widgets
from sys import exit
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QListWidgetItem
from PyQt5.QtWidgets import QLineEdit, QLabel, QListWidget, QMessageBox

# -----------------------------------------------------------------------
class WorkerThread(Thread):

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

def main(argv):

    if len(argv) != 3:
        print('Usage: reg host port')
        exit(1)
    try:
        argv[2] = int(argv[2])
    except:
        print('Port must be an integer')
        exit(1)

    app = QApplication([])
    #button = QPushButton('Submit')
    listWidget = QListWidget()

    LineEdit1 = QLineEdit('')
    LineEdit2 = QLineEdit('')
    LineEdit3 = QLineEdit('')
    LineEdit4 = QLineEdit('')

    deptLabel = QLabel('Department:')
    coursenumLabel = QLabel('Number:')
    areaLabel = QLabel('Area:')
    titleLabel = QLabel('Title:')

    outputLayout = QGridLayout()
    outputLayout.setRowStretch(0, 0)
    outputLayout.setColumnStretch(0, 0)
    #outputLayout.addWidget(button, 0, 0)
    outputLayout.addWidget(listWidget, 1, 0)
    outputFrame = QFrame()
    outputFrame.setLayout(outputLayout)

    inputLayout = QGridLayout()
    inputLayout.setSpacing(0)
    inputLayout.addWidget(deptLabel, 0, 1)
    inputLayout.addWidget(coursenumLabel, 1, 1)
    inputLayout.addWidget(areaLabel, 2, 1)
    inputLayout.addWidget(titleLabel, 3, 1)
    inputLayout.addWidget(LineEdit1, 0, 2)
    inputLayout.addWidget(LineEdit2, 1, 2)
    inputLayout.addWidget(LineEdit3, 2, 2)
    inputLayout.addWidget(LineEdit4, 3, 2)
    inputFrame = QFrame()
    inputFrame.setLayout(inputLayout)

    submitLayout = QGridLayout()
    submitLayout.addWidget(button, 0, 0)
    submitFrame = QFrame()
    submitFrame.setLayout(submitLayout)

    topLayout = QGridLayout()
    topLayout.addWidget(inputFrame, 0, 0)
    topLayout.addWidget(submitFrame, 0, 1)
    topFrame = QFrame()
    topFrame.setLayout(topLayout)

    FrameLayout = QGridLayout()
    FrameLayout.setContentsMargins(0, 0, 0, 0)
    FrameLayout.setRowStretch(1, 0)
    FrameLayout.setColumnStretch(1, 0)
    FrameLayout.addWidget(outputFrame, 1, 0)
    FrameLayout.addWidget(topFrame, 0, 0)
    Frame = QFrame()
    Frame.setLayout(FrameLayout)

    window = QMainWindow()
    window.setWindowTitle('Princeton University Class Search')
    window.setCentralWidget(Frame)
    screenSize = QDesktopWidget().screenGeometry()
    window.resize(screenSize.width() // 2, screenSize.height() // 2)

    args = [argv[0]]
    args.append("-h")
    print('Sent command: getOverview')

    try:
        host = argv[1]
        port = int(argv[2])

        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
        flowrite = sock.makefile(mode='wb')
        dump(args, flowrite)
        flowrite.flush()
        floread = sock.makefile(mode='rb')
        output = load(floread)
        sock.close()

    except Exception as e:
        print(e, file=stderr)

    try:
        if output[0] == 1:
            window.show()
        else:
            for item in output[1]:
                listWidget.addItem(item)
            window.show()
    except:
        error = QMessageBox.information(window, 'Server Error', "Server is unavailable")

    def buttonSlot():
        listWidget.clear()
        args = [argv[0]]
        args.append("-h")
        if LineEdit1.text() != '':
            args.append('-dept')
            args.append(LineEdit1.text())
        if LineEdit2.text() != '':
            args.append('-coursenum')
            args.append(LineEdit2.text())
        if LineEdit3.text() != '':
            args.append('-area')
            args.append(LineEdit3.text())
        if LineEdit4.text() != '':
            args.append('-title')
            args.append(LineEdit4.text())

        #output = managedb(args)
        print('Sent command: getOverview')
        try:
            host = argv[1]
            port = int(argv[2])

            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((host, port))
            flowrite = sock.makefile(mode='wb')
            dump(args, flowrite)
            flowrite.flush()
            floread = sock.makefile(mode='rb')
            output = load(floread)
            sock.close()

            if output[0] == 1:
                window.show()
                error = QMessageBox.information(window, 'Database Error', output[1][0])
            elif output[0] == 2:
                window.show()
                error = QMessageBox.information(window, 'Database Error', "Database is corrupted")
            else:
                for item in output[1]:
                    listWidget.addItem(item)

        except Exception as e:
            print(e, file=stderr)
            window.show()

    def handleClick():
        item = listWidget.currentItem()
        text = item.text()
        itemcoursenum = text[0:text.index(' ')]
        detailargs = ['regdetails.py', '-h', itemcoursenum]
        print('Sent command: getDetail')
        try:
            host = argv[1]
            port = int(argv[2])

            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((host, port))
            flowrite = sock.makefile(mode='wb')
            dump(detailargs, flowrite)
            flowrite.flush()
            floread = sock.makefile(mode='rb')
            finalStr = load(floread)
            sock.close()
            reply = QMessageBox.information(window, 'Class Details', finalStr)
        except Exception as e:
            error = QMessageBox.information(window, 'Server Error', 'Server is Unavailable')
            print("testing error server crashed")
            print(e, file=stderr)

    try:
        button.clicked.connect(buttonSlot)
        LineEdit1.returnPressed.connect(buttonSlot)
        LineEdit2.returnPressed.connect(buttonSlot)
        LineEdit3.returnPressed.connect(buttonSlot)
        LineEdit4.returnPressed.connect(buttonSlot)
        listWidget.itemActivated.connect(handleClick)
    except:
        error = QMessageBox.information(window, 'Server Error', 'Server is unavailable')
        print(e, file=stderr)

    window.show()
    exit(app.exec_())

if __name__ == '__main__':
    main(argv)

