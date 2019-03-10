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

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGroupBox, QGridLayout, QSlider, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator

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
        
        self.convolution = Convolution()
        
        self.initUI()
        
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
        self.tminLabel = QLabel("Valeur minimum de t")
        self.tminLabel.setAlignment(Qt.AlignRight)
        self.tmaxLabel = QLabel("Valeur maximum de t")
        self.tmaxLabel.setAlignment(Qt.AlignRight)
        self.XFunctionLabel = QLabel("Fonction x(t)")
        self.XFunctionLabel.setAlignment(Qt.AlignRight)
        self.HFunctionLabel = QLabel("Fonction h(t)")
        self.HFunctionLabel.setAlignment(Qt.AlignRight)
        self.MessageLabel = QLabel("Les fonctions doivent être entrées avec" + 
                                   " la syntaxe Python. Numpy est disponible" +
                                   " sous le raccourci \"np\".")
        self.MessageLabel.setAlignment(Qt.AlignCenter)
        
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.moveTau) 
        self.slider.setTickPosition(QSlider.TicksBelow)
        
        self.tminInput = QLineEdit()
        self.tminInput.setValidator(QDoubleValidator())
        self.tminInput.textChanged.connect(self.updateMinRange)
        
        self.tmaxInput = QLineEdit()
        self.tmaxInput.setValidator(QDoubleValidator())
        self.tmaxInput.textChanged.connect(self.updateMaxRange)
        
        self.XFunctionInput = QLineEdit()
        self.HFunctionInput = QLineEdit()
        
        
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
        layout.addWidget(self.canvasResult, 2, 2, 9, 1)
        layout.addWidget(self.sliderLabel, 2, 0, 1, 2)
        layout.addWidget(self.slider, 3, 0, 1, 2)
        layout.addWidget(self.buttonReset, 5,0)
        layout.addWidget(self.buttonUpdate, 5,1)
        layout.addWidget(self.tminInput, 6,1)
        layout.addWidget(self.tmaxInput, 7,1)
        layout.addWidget(self.XFunctionInput, 8,1)
        layout.addWidget(self.HFunctionInput, 9,1)
        layout.addWidget(self.tminLabel, 6,0)
        layout.addWidget(self.tmaxLabel, 7,0)
        layout.addWidget(self.XFunctionLabel, 8,0)
        layout.addWidget(self.HFunctionLabel, 9,0)
        layout.addWidget(self.MessageLabel, 10,0, 1, 2)
        
        self.setLayout(layout)

    def plotDefaults(self):
        
        self.convolution.setRange(0, 10)
        self.convolution.setTau(1)
        self.tminInput.clear()
        self.tmaxInput.clear()
        self.XFunctionInput.clear()
        self.HFunctionInput.clear()

        self.figureX.clear()
        ax = self.figureX.add_subplot(111)
        dataX = self.convolution.getXfunction()
        ax.plot(dataX[0], dataX[1])
        ax.set_title("x(t)")
        self.canvasX.draw()

        self.figureH.clear()
        ax = self.figureH.add_subplot(111)
        dataH = self.convolution.getHfunction()
        ax.plot(dataH[0], dataH[1])
        ax.set_title("h(t)")
        self.canvasH.draw()
        
        self.figureRelative.clear()
        ax = self.figureRelative.add_subplot(111)
        tau = self.convolution.getTau()
        ax.plot(dataX[0], dataX[1], color='blue')
        ax.plot(dataH[0]+tau, dataH[1], color='green')
        ax.axvline(x=tau, color='red')
        ax.set_title("Positions relatives de x(t) et h(t)")
        self.canvasRelative.draw()
        
        self.figureProducts.clear()
        ax = self.figureProducts.add_subplot(111)
        ax.axvline(x=tau, color='red')
        ax.set_title("Translation de h(t) en un point")
        self.canvasProducts.draw()
        
        self.figureResult.clear()
        ax = self.figureResult.add_subplot(111)
        ax.set_title("Convolution x(t) et h(t)")
        data = self.convolution.getConvolution()
        ax.plot(data[0], data[1])
        self.canvasResult.draw()
        
        self.slider.setTickPosition(self.convolution.getMinRange())
        self.slider.setTickInterval(self.convolution.getStep())
        self.slider.setSingleStep((self.convolution.getMaxRange()-self.convolution.getMinRange())/100)
        
    def plotUpdate(self):
        self.figureX.clear()
        ax = self.figureX.add_subplot(111)
        dataX = self.convolution.getXfunction()
        ax.plot(dataX[0], dataX[1])
        ax.set_title("x(t)")
        self.canvasX.draw()

        self.figureH.clear()
        ax = self.figureH.add_subplot(111)
        dataH = self.convolution.getHfunction()
        ax.plot(dataH[0], dataH[1])
        ax.set_title("h(t)")
        self.canvasH.draw()
        
        self.figureRelative.clear()
        ax = self.figureRelative.add_subplot(111)
        tau = self.convolution.getTau()
        ax.plot(dataX[0], dataX[1], color='blue')
        ax.plot(dataH[0]+tau, dataH[1], color='green')
        ax.axvline(x=tau, color='red')
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
    
    def updateMinRange(self, minvalue):
        self.convolution.setMinRange(float(minvalue))
        self.plotUpdate()
        
    def updateMaxRange(self, maxvalue):
        self.convolution.setMaxRange(float(maxvalue))
        self.plotUpdate()
    
    def moveTau(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()

    sys.exit(app.exec_())
    