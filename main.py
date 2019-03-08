#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a small tool to help people learn, visualize  and understand how 
convolution operates by reconstructing the convolution integral graphically.

Ce programme est un outil visant à aider l'apprentissage, la visualisation et 
la compréhension de la convolution en contruisant graphiquement l'intégral de
convolution.

License : GPL 3
"""

import numpy as np
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from convolution import Convolution

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 50
        self.top = 50
        self.width = 1600
        self.height = 900
        self.initUI()
        self.convolution = Convolution()
        self.plotDefaults()
        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
        
        self.createCanvas()
        self.createWidgets()

        self.createGridLayout()
        

    def createCanvas(self):
        # Figure and canvas instances - canvas takes the `figure` instance as a parameter to __init__
        self.figureX = plt.figure()
        self.figureH = plt.figure()
        self.figureRelative = plt.figure()
        self.figureResult = plt.figure()
        self.canvasX = FigureCanvas(self.figureX)
        self.canvasH = FigureCanvas(self.figureH)
        self.canvasRelative = FigureCanvas(self.figureRelative)
        self.canvasResult  = FigureCanvas(self.figureResult )

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        # self.toolbarX = NavigationToolbar(self.canvasX, self)
        
    def createWidgets(self):
        
        #Button Widegets
        # Just some button connected to `plot` method
        self.buttonUpdate = QPushButton('Update ALL')
        self.buttonUpdate.clicked.connect(self.plotDefaults)
        
        
    def createGridLayout(self):
        # set the layout
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(1, 100)
        layout.setColumnStretch(1, 100)
        layout.setColumnStretch(2, 200)
        layout.addWidget(self.canvasX, 0, 0)
        layout.addWidget(self.canvasH, 0, 1)
        layout.addWidget(self.canvasRelative, 0, 2)
        layout.addWidget(self.canvasResult, 2, 2)
        layout.addWidget(self.buttonUpdate, 2,0)
        self.setLayout(layout)

    def plotDefaults(self):

        self.figureX.clear()
        ax = self.figureX.add_subplot(111)
        data = self.convolution.getXfunction()
        ax.plot(data[0], data[1])

        self.canvasX.draw()

        self.figureH.clear()
        ax = self.figureH.add_subplot(111)
        data = self.convolution.getHfunction()
        ax.plot(data[0], data[1])
        self.canvasH.draw()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()

    sys.exit(app.exec_())
    