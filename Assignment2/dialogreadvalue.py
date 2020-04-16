#!/usr/bin/env python

# -----------------------------------------------------------------------
# dialogreadvalue.py
# Author: Bob Dondero
# -----------------------------------------------------------------------

from sys import exit
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtWidgets import QTextEdit, QInputDialog


def main():
    app = QApplication([])

    button = QPushButton('Show Dialog')

    textEdit = QTextEdit()

    layout = QGridLayout()
    layout.addWidget(button, 0, 0)
    layout.addWidget(textEdit, 1, 0)
    layout.setRowStretch(0, 0)
    layout.setRowStretch(1, 1)

    frame = QFrame()
    frame.setLayout(layout)

    window = QMainWindow()
    window.setWindowTitle('Read a value')
    window.setCentralWidget(frame)
    screenSize = QDesktopWidget().screenGeometry()
    window.resize(screenSize.width() // 2, screenSize.height() // 2)

    def buttonSlot():
        reply, successful = \
            QInputDialog.getText(window, 'My title', 'My prompt')
        if successful:
            textEdit.append(reply)
        else:
            textEdit.append('(no reply)')

    button.clicked.connect(buttonSlot)

    window.show()
    exit(app.exec_())


if __name__ == '__main__':
    main()