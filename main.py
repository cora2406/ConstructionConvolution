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

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGroupBox, QGridLayout, QSlider, QLabel, QLineEdit, QRadioButton
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
        
        self.sliderTimeFactor = 10
        self.modeEcho = True
        
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
        self.buttonEcho = QRadioButton('Mode echo')
        self.buttonEcho.clicked.connect(self.setModeEcho)
        self.buttonReverse = QRadioButton('Mode retourné')
        self.buttonReverse.clicked.connect(self.setModeReverse)
        
        
        self.sliderTimeLabel = QLabel("Selection du point t à évaluer")
        self.sliderTimeLabel.setAlignment(Qt.AlignCenter)
        self.sliderEchoLabel = QLabel("Nombre d'echos")
        self.sliderEchoLabel.setAlignment(Qt.AlignCenter)
        self.tminXLabel = QLabel("Valeur minimum de t pout x(t)")
        self.tminXLabel.setAlignment(Qt.AlignRight)
        self.tmaxXLabel = QLabel("Valeur maximum de t pour x(t)")
        self.tmaxXLabel.setAlignment(Qt.AlignRight)
        self.tminHLabel = QLabel("Valeur minimum de t pour h(t)")
        self.tminHLabel.setAlignment(Qt.AlignRight)
        self.tmaxHLabel = QLabel("Valeur maximum de t pour h(t)")
        self.tmaxHLabel.setAlignment(Qt.AlignRight)
        self.XFunctionLabel = QLabel("Fonction x(t)")
        self.XFunctionLabel.setAlignment(Qt.AlignRight)
        self.HFunctionLabel = QLabel("Fonction h(t)")
        self.HFunctionLabel.setAlignment(Qt.AlignRight)
        self.MessageLabel = QLabel("Les fonctions doivent être entrées avec" + 
                                   " la syntaxe Python et la nomenclature Numpy. " +
                                   "Il y a 1000 points dans le vecteur \"t\".")
        self.MessageLabel.setAlignment(Qt.AlignCenter)
        
        
        self.sliderTime = QSlider(Qt.Horizontal)
        self.sliderTime.valueChanged.connect(self.moveTau) 
        self.sliderTime.setTickPosition(QSlider.TicksBelow)
        
        self.sliderEcho = QSlider(Qt.Horizontal)
        self.sliderEcho.valueChanged.connect(self.changeNumberOfEchos) 
        self.sliderEcho.setTickPosition(QSlider.TicksBelow)
        
        self.sliderEcho.setMinimum(1)
        self.sliderEcho.setMaximum(300)
        
        self.tminXInput = QLineEdit()
        self.tminXInput.setValidator(QDoubleValidator())
        self.tminXInput.textChanged.connect(self.updateMinRangeX)
        
        self.tmaxXInput = QLineEdit()
        self.tmaxXInput.setValidator(QDoubleValidator())
        self.tmaxXInput.textChanged.connect(self.updateMaxRangeX)
        
        self.tminHInput = QLineEdit()
        self.tminHInput.setValidator(QDoubleValidator())
        self.tminHInput.textChanged.connect(self.updateMinRangeH)
        
        self.tmaxHInput = QLineEdit()
        self.tmaxHInput.setValidator(QDoubleValidator())
        self.tmaxHInput.textChanged.connect(self.updateMaxRangeH)
        
        self.XFunctionInput = QLineEdit()
        self.XFunctionInput.returnPressed.connect(self.updateXFunction)
        self.HFunctionInput = QLineEdit()
        self.HFunctionInput.returnPressed.connect(self.updateHFunction)
        
        
    def createGridLayout(self):
        # set the layout
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(0, 50)
        layout.setColumnStretch(2, 50)
        layout.setColumnStretch(4, 1000)
        layout.addWidget(self.canvasX, 0, 0, 1, 2)
        layout.addWidget(self.canvasH, 0, 2, 1, 2)
        layout.addWidget(self.canvasRelative, 1, 0, 1, 4)
        layout.addWidget(self.canvasProducts, 0, 4, 2, 1)
        layout.addWidget(self.canvasResult, 2, 4, 10, 1)
        layout.addWidget(self.sliderTimeLabel, 2, 0, 1, 4)
        layout.addWidget(self.sliderTime, 3, 0, 1, 4)
        layout.addWidget(self.sliderEcho, 4, 0, 1, 4)
        layout.addWidget(self.sliderEcho, 5, 0, 1, 4)
        layout.addWidget(self.buttonReset, 6, 0)
        layout.addWidget(self.buttonUpdate, 6, 1)
        
        layout.addWidget(self.buttonEcho, 6, 2)
        layout.addWidget(self.buttonReverse, 6, 3)
        
        layout.addWidget(self.tminXLabel, 7,0)
        layout.addWidget(self.tmaxXLabel, 8,0)
        layout.addWidget(self.tminXInput, 7,1)
        layout.addWidget(self.tmaxXInput, 8,1)
        
        layout.addWidget(self.tminHLabel, 7,2)
        layout.addWidget(self.tmaxHLabel, 8,2)
        layout.addWidget(self.tminHInput, 7,3)
        layout.addWidget(self.tmaxHInput, 8,3)
        
        layout.addWidget(self.XFunctionInput, 9,1,1,3)
        layout.addWidget(self.HFunctionInput, 10,1,1,3)
        layout.addWidget(self.XFunctionLabel, 9,0,1,1)
        layout.addWidget(self.HFunctionLabel, 10,0, 1,1)
        layout.addWidget(self.MessageLabel, 11,0, 1, 4)
        
        self.setLayout(layout)

    def plotDefaults(self):
        
        self.convolution = Convolution()
        self.tminXInput.clear()
        self.tmaxXInput.clear()
        self.tminHInput.clear()
        self.tmaxHInput.clear()
        self.XFunctionInput.clear()
        self.HFunctionInput.clear()

        self.plotUpdate()
        
        self.updateSlider()
        
    def updateSlider(self):
        self.sliderTime.setMinimum(self.convolution.getMinRangeX()*self.sliderTimeFactor)
        self.sliderTime.setMaximum(self.convolution.getMaxRangeX()*self.sliderTimeFactor)
        #self.sliderTime.setTickInterval(self.convolution.getStep())
        self.sliderTime.setSingleStep((self.convolution.getMaxRangeX()-self.convolution.getMinRangeX())/100)
        
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
        ax.axvline(x=tau, color='red')
        ax.plot((dataH[0]-dataH[0][0]+tau), dataH[1], color='green')
        ax.text(0.9, 0.9, 't = {}'.format(tau), transform=ax.transAxes, fontsize='large')
        ax.set_title("Positions relatives de x(t) et h(t)")
        self.canvasRelative.draw()
        
        
        tauindex = int(((tau-self.convolution.getMinRangeX())/self.convolution.getStep()))
        
        self.figureResult.clear()
        ax = self.figureResult.add_subplot(111)
        ax.set_title("Convolution x(t) et h(t)")
        data = self.convolution.getConvolution()
        ax.plot(data[0], data[1])
        ax.axvline(x=tau, color='red')
        ax.scatter(tau, data[1][tauindex])
        ax.text(0.8, 0.9, 'x(t) * h(t) = {0:5.4f}'.format(data[1][tauindex]), transform=ax.transAxes, fontsize='large')
        self.canvasResult.draw()
        
        if self.modeEcho == True:
            self.productPlotWithEchos()
        else:
            self.productPlotReverse()
        
    def productPlotWithEchos(self):
        self.figureProducts.clear()
        
        tau = self.convolution.getTau()
        dataX = self.convolution.getXfunction()
        dataH = self.convolution.getHfunction()
        
        ax = self.figureProducts.add_subplot(111)
        ax.axvline(x=tau, color='red')
        ax.plot(dataX[0], dataX[1], color='blue')
        ax.plot((dataH[0]-dataH[0][0]+tau), dataH[1], color='green')
        tauindex = int(((tau-self.convolution.getMinRangeX())/self.convolution.getStep()))
        ax.text(0.7, 0.95, r'$\Delta\tau=$ {0:5.4f}'.format(self.convolution.getEchoPoints()*self.convolution.getStep()), transform=ax.transAxes, fontsize='large')
        textincrement = 0
        total=dataH[1][0]*dataX[1][tauindex]*self.convolution.getEchoPoints()*self.convolution.getStep()
        ax.scatter(tau, dataX[1][tauindex], marker='x')
        for i, echo in enumerate(self.convolution.createEchos()):
            try:
                intersection = (dataX[1][i*(self.convolution.getEchoPoints())]*
                                dataH[1][self.convolution.getHindex(echo-self.convolution.getMinRangeX()+self.convolution.getMinRangeH())])
            except IndexError:
                intersection = 0
                
            if intersection>0:
                tOffset = dataH[0][0]-tau+echo-self.convolution.getMinRangeX()
                line, = ax.plot((dataH[0]-tOffset), dataX[1][i*(self.convolution.getEchoPoints())] * dataH[1], alpha = 0.5)
                ax.scatter(tau, intersection, color=line.get_color())
                if textincrement < 16:
                    ax.text(0.7, 0.9-textincrement*0.05, 
                            r'$x(t-\tau_{{{0}}})h(\tau_{{{0}}}) =$ {1:5.4f}'.format(textincrement+1, intersection), 
                            transform=ax.transAxes, fontsize='large', color=line.get_color())
                    textincrement+=1
                total += intersection*self.convolution.getEchoPoints()*self.convolution.getStep()
                
        ax.text(0.95, 0.1, r"$\sum{{x(t-\tau_{{n}})\cdot h(\tau_{{n}})\cdot\Delta\tau}}=${0:5.2f}".format(total), transform=ax.transAxes, fontsize='x-large', ha='right')
        ax.set_title("Translation de h(t) en un point")
        self.canvasProducts.draw()
    
    def productPlotReverse(self):
        self.figureProducts.clear()
                
        tau = self.convolution.getTau()
        dataX = self.convolution.getXfunction()
        dataH = self.convolution.getHfunction()
        
        ax = self.figureProducts.add_subplot(111)
        ax.axvline(x=tau, color='red')
        ax.plot(dataX[0], dataX[1], color='blue')
        ax.plot((-dataH[0]+tau), dataH[1], color='green')
        tauindex = int(((tau-self.convolution.getMinRangeX())/self.convolution.getStep()))
        ax.text(0.7, 0.95, r'$\Delta\tau=$ {0:5.4f}'.format(self.convolution.getEchoPoints()*self.convolution.getStep()), transform=ax.transAxes, fontsize='large')
        textincrement = 0
        total=dataH[1][0]*dataX[1][tauindex]*self.convolution.getEchoPoints()*self.convolution.getStep()
        ax.scatter(tau, dataX[1][tauindex], marker='x')
        for i, echo in enumerate(self.convolution.createEchos()):
            try:
                intersection = (dataX[1][i*(self.convolution.getEchoPoints())]*
                                dataH[1][self.convolution.getHindex(echo-self.convolution.getMinRangeX()+
                                     self.convolution.getMinRangeH())])
            except IndexError:
                intersection = 0
                
            if intersection>0:
                ax.axvline(x=tau-echo)
                #Find color and apply to scatter and text
                ax.scatter(tau-echo, intersection)
                if textincrement < 16:
                    ax.text(0.7, 0.9-textincrement*0.05, 
                            r'$x(t-\tau_{{{0}}})h(\tau_{{{0}}}) =$ {1:5.4f}'.format(textincrement+1, intersection), 
                            transform=ax.transAxes, fontsize='large')
                    textincrement+=1
                total += intersection*self.convolution.getEchoPoints()*self.convolution.getStep()
                
        ax.text(0.95, 0.1, r"$\sum{{x(tau_{{n}})\cdot h(t-\tau_{{n}})\cdot\Delta\tau}}=${0:5.2f}".format(total), transform=ax.transAxes, fontsize='x-large', ha='right')
        ax.set_title("Translation de h(t) en un point")
        #SET Axes to fix X
        self.canvasProducts.draw()
        
    
    def updateMinRangeX(self, minvalue):
        self.convolution.setMinRangeX(float(minvalue))
        self.plotUpdate()
        self.updateSlider()
        
    def updateMaxRangeX(self, maxvalue):
        self.convolution.setMaxRangeX(float(maxvalue))
        self.plotUpdate()
        self.updateSlider()
        
    def updateMinRangeH(self, minvalue):
        self.convolution.setMinRangeH(float(minvalue))
        self.plotUpdate()
        self.updateSlider()
        
    def updateMaxRangeH(self, maxvalue):
        self.convolution.setMaxRangeH(float(maxvalue))
        self.plotUpdate()
        self.updateSlider()
        
    def updateXFunction(self):
        self.convolution.setXFunction(self.XFunctionInput.text())
        self.plotUpdate()
        
    def updateHFunction(self):
        self.convolution.setHFunction(self.HFunctionInput.text())
        self.plotUpdate()
    
    def moveTau(self):
        tau = self.sliderTime.value()/float(self.sliderTimeFactor)
        self.convolution.setTau(tau)
        self.plotUpdate()
        
    def changeNumberOfEchos(self):
        self.convolution.setEchoRate(self.sliderEcho.value())
        self.plotUpdate()
        
    def setModeEcho(self):
        self.modeEcho = True
        self.productPlotWithEchos()
        
    def setModeReverse(self):
        self.modeEcho = False
        self.productPlotReverse()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = App()

    sys.exit(app.exec_())
    