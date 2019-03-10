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

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGroupBox, QGridLayout, QSlider, QLabel
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from convolution import Convolution

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'La construction de la convolution'
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
        self.figureProducts = plt.figure()
        self.canvasX = FigureCanvas(self.figureX)
        self.canvasH = FigureCanvas(self.figureH)
        self.canvasRelative = FigureCanvas(self.figureRelative)
        self.canvasResult  = FigureCanvas(self.figureResult )
        self.canvasProducts  = FigureCanvas(self.figureProducts)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        # self.toolbarX = NavigationToolbar(self.canvasX, self)
        
    def createWidgets(self):
        
        #Button Widgets
        self.buttonReset = QPushButton('Réinitialisation')
        self.buttonReset.clicked.connect(self.plotDefaults)
        self.buttonUpdate = QPushButton('Mettre à jour les graphiques')
        self.buttonUpdate.clicked.connect(self.plotUpdate)
        
        self.sliderLabel = QLabel("Selection de tau")
        self.sliderLabel.setAlignment(Qt.AlignCenter)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.moveTau) 
        self.slider.setTickPosition(QSlider.TicksBelow)
        
        
    def createGridLayout(self):
        # set the layout
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(0, 100)
        layout.setColumnStretch(1, 100)
        layout.setColumnStretch(2, 300)
        layout.addWidget(self.canvasX, 0, 0)
        layout.addWidget(self.canvasH, 0, 1)
        layout.addWidget(self.canvasRelative, 1, 0, 1, 2)
        layout.addWidget(self.canvasProducts, 0, 2, 2, 1)
        layout.addWidget(self.canvasResult, 2, 2, 3, 1)
        layout.addWidget(self.sliderLabel, 2, 0, 1, 2)
        layout.addWidget(self.slider, 3, 0, 1, 2)
        layout.addWidget(self.buttonReset, 4,0)
        layout.addWidget(self.buttonUpdate, 4,1)
        self.setLayout(layout)

    def plotDefaults(self):

        self.figureX.clear()
        ax = self.figureX.add_subplot(111)
        data = self.convolution.getXfunction()
        ax.plot(data[0], data[1])
        ax.set_title("x(t)")
        self.canvasX.draw()

        self.figureH.clear()
        ax = self.figureH.add_subplot(111)
        data = self.convolution.getHfunction()
        ax.plot(data[0], data[1])
        ax.set_title("h(t)")
        self.canvasH.draw()
        
        self.figureRelative.clear()
        ax = self.figureRelative.add_subplot(111)
        ax.set_title("Positions relatives de x(t) et h(t)")
        self.canvasRelative.draw()
        
        self.figureProducts.clear()
        ax = self.figureProducts.add_subplot(111)
        ax.set_title("Translation de h(t) en un point")
        self.canvasProducts.draw()
        
        self.figureResult.clear()
        ax = self.figureResult.add_subplot(111)
        ax.set_title("Convolution x(t) et h(t)")
        data = self.convolution.getConvolution()
        ax.plot(data[0], data[1])
        self.canvasResult.draw()
        
        #self.slider.setTickPosition(0)
        #self.slider.setTickInterval(10)
        #self.slider.setSingleStep(1)
        
    def plotUpdate(self):
        pass
    
    def moveTau(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()

    sys.exit(app.exec_())
    