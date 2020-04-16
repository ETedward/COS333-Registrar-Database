#!/usr/bin/env python

# -----------------------------------------------------------------------
# colordisplayer.py
# Author: Bob Dondero
# -----------------------------------------------------------------------

from sys import exit
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QLabel, QSlider, QLineEdit, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


def main():
    MAX_INTENSITY = 255

    app = QApplication([])

    # Create and lay out widgets.

    redLabel = QLabel('Red:')
    redLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    redLabel.setAutoFillBackground(True)
    p = redLabel.palette()
    p.setColor(redLabel.backgroundRole(), Qt.red)
    redLabel.setPalette(p)

    greenLabel = QLabel('Green:')
    greenLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    greenLabel.setAutoFillBackground(True)
    p = greenLabel.palette()
    p.setColor(greenLabel.backgroundRole(), Qt.green)
    greenLabel.setPalette(p)

    blueLabel = QLabel('Blue:')
    blueLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    blueLabel.setAutoFillBackground(True)
    p = blueLabel.palette()
    p.setColor(blueLabel.backgroundRole(), Qt.blue)
    blueLabel.setPalette(p)

    redSlider = QSlider(Qt.Horizontal)
    redSlider.setMinimum(0)
    redSlider.setMaximum(MAX_INTENSITY)

    greenSlider = QSlider(Qt.Horizontal)
    greenSlider.setMinimum(0)
    greenSlider.setMaximum(MAX_INTENSITY)

    blueSlider = QSlider(Qt.Horizontal)
    blueSlider.setMinimum(0)
    blueSlider.setMaximum(MAX_INTENSITY)

    redLineEdit = QLineEdit('0')
    greenLineEdit = QLineEdit('0')
    blueLineEdit = QLineEdit('0')

    controlFrameLayout = QGridLayout()
    controlFrameLayout.setSpacing(0)
    controlFrameLayout.setContentsMargins(0, 0, 0, 0)
    controlFrameLayout.setRowStretch(0, 0)
    controlFrameLayout.setRowStretch(1, 0)
    controlFrameLayout.setRowStretch(2, 0)
    controlFrameLayout.setColumnStretch(0, 0)
    controlFrameLayout.setColumnStretch(1, 1)
    controlFrameLayout.setColumnStretch(2, 0)
    controlFrameLayout.addWidget(redLabel, 0, 0)
    controlFrameLayout.addWidget(greenLabel, 1, 0)
    controlFrameLayout.addWidget(blueLabel, 2, 0)
    controlFrameLayout.addWidget(redSlider, 0, 1)
    controlFrameLayout.addWidget(greenSlider, 1, 1)
    controlFrameLayout.addWidget(blueSlider, 2, 1)
    controlFrameLayout.addWidget(redLineEdit, 0, 2)
    controlFrameLayout.addWidget(greenLineEdit, 1, 2)
    controlFrameLayout.addWidget(blueLineEdit, 2, 2)
    controlFrame = QFrame()
    controlFrame.setLayout(controlFrameLayout)

    colorFrame = QFrame()
    colorFrame.setAutoFillBackground(True)
    p = colorFrame.palette()
    p.setColor(colorFrame.backgroundRole(), Qt.black)
    colorFrame.setPalette(p)

    centralFrameLayout = QGridLayout()
    centralFrameLayout.setSpacing(0)
    centralFrameLayout.setContentsMargins(0, 0, 0, 0)
    centralFrameLayout.setRowStretch(0, 1)
    centralFrameLayout.setRowStretch(1, 0)
    centralFrameLayout.setColumnStretch(0, 1)
    centralFrameLayout.addWidget(colorFrame, 0, 0)
    centralFrameLayout.addWidget(controlFrame, 1, 0)
    centralFrame = QFrame()
    centralFrame.setLayout(centralFrameLayout)

    window = QMainWindow()
    window.setWindowTitle('Color Displayer')
    window.setCentralWidget(centralFrame)
    screenSize = QDesktopWidget().screenGeometry()
    window.resize(screenSize.width() // 2, screenSize.height() // 2)

    # Handle events for the QSlider objects.

    def sliderSlot():
        r = redSlider.value()
        g = greenSlider.value()
        b = blueSlider.value()
        redLineEdit.setText(str(r))
        greenLineEdit.setText(str(g))
        blueLineEdit.setText(str(b))
        p = colorFrame.palette()
        p.setColor(colorFrame.backgroundRole(), QColor(r, g, b))
        colorFrame.setPalette(p)

    redSlider.valueChanged.connect(sliderSlot)
    greenSlider.valueChanged.connect(sliderSlot)
    blueSlider.valueChanged.connect(sliderSlot)

    # Handle events for the LineEdit objects.

    def lineEditSlot():
        try:
            r = int(redLineEdit.text())
            g = int(greenLineEdit.text())
            b = int(blueLineEdit.text())
            if (r < 0) or (r > MAX_INTENSITY): raise Exception()
            if (g < 0) or (g > MAX_INTENSITY): raise Exception()
            if (b < 0) or (b > MAX_INTENSITY): raise Exception()
            redSlider.setValue(r)
            greenSlider.setValue(g)
            blueSlider.setValue(b)
            p = colorFrame.palette()
            p.setColor(colorFrame.backgroundRole(), QColor(r, g, b))
            colorFrame.setPalette(p)
        except:
            # Use the Slider objects to restore the LineEdit objects.
            redLineEdit.setText(str(redSlider.value()))
            greenLineEdit.setText(str(greenSlider.value()))
            blueLineEdit.setText(str(blueSlider.value()))

    redLineEdit.returnPressed.connect(lineEditSlot)
    greenLineEdit.returnPressed.connect(lineEditSlot)
    blueLineEdit.returnPressed.connect(lineEditSlot)

    window.show()
    exit(app.exec_())


if __name__ == '__main__':
    main()