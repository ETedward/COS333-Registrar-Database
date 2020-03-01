#!/usr/bin/env python

# -----------------------------------------------------------------------
# dialogchooseoption.py
# Author: Bob Dondero
# -----------------------------------------------------------------------

from sys import exit
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtWidgets import QTextEdit, QMessageBox


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
    window.setWindowTitle('Choose an option')
    window.setCentralWidget(frame)
    screenSize = QDesktopWidget().screenGeometry()
    window.resize(screenSize.width() // 2, screenSize.height() // 2)

    def buttonSlot():
        reply = QMessageBox.question(window, 'My title', 'My message',
                                     buttons=(QMessageBox.Yes | QMessageBox.No))
        # Others: Ok, Open, Save, Cancel, Close, Discard,
        # Apply, Reset, RestoreDefaults, Help, SaveAll,
        # YesToAll, NoToAll, Abort, Retry, Ignore, NoButton
        if reply == QMessageBox.Yes:
            text = 'Yes'
        elif reply == QMessageBox.No:
            text = 'No'
        else:
            text = '(No option chosen)'  # Unused!!!
        textEdit.append(text)

    button.clicked.connect(buttonSlot)

    window.show()
    exit(app.exec_())


if __name__ == '__main__':
    main()