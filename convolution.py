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

__author__ = "Audrey Corbeil Therrien"
__copyright__ = '2019, ConstructionConvolution'
__credits__ = ["Audrey Corbeil Therrien"]
__license__ = "GPL 3"
__version__ = "0.0.1"
__maintainer__ = "Audrey Corbeil Therrien"
__email__ = "therria@stanford.edu"
__status__ = "Prototype"

class Convolution:
    def __init__(self):
        self.minrangeX = 0
        self.maxrangeX = 10
        self.minrangeH = 0
        self.maxrangeH = 10
        self.tau = 1
        self.points = 1000;
        self.step = (self.maxrangeX - self.minrangeX)/self.points
        self.echoPoints = int(self.points/20)
        self.rangeX = np.arange(self.minrangeX, self.maxrangeX, self.step)
        self.rangeH = np.arange(self.minrangeH, self.maxrangeH, self.step)
        
    def getMinRangeX(self):
        return self.minrangeX
    
    def getMinRangeH(self):
        return self.minrangeH
    
    def getMaxRangeX(self):
        return self.maxrangeX
    
    def getMaxRangeH(self):
        return self.maxrangeH
    
    def getStep(self):
        return self.step
    
    def getEchoPoints(self):
        return self.echoPoints
    
    def getTau(self):
        return self.tau
        
    def getXfunction(self):
        self.x = np.hstack((np.zeros(200), np.ones(300), np.zeros(500)))
        return [self.rangeX, self.x]
    
    def getHfunction(self):
        self.h = np.exp(-self.rangeH)
        return [self.rangeH, self.h]
    
    def getConvolution(self):
        self.result = np.convolve(self.x, self.h)*self.step
        self.convolveRange = np.linspace(self.minrangeX, self.minrangeX+(self.result.size*self.step), num=self.result.size)
        return [self.convolveRange, self.result]


    def setMinRangeX(self, newmin):
        self.minrangeX = newmin
        self.step = (self.maxrangeX - self.minrangeX)/self.points
        self.rangeX = np.arange(self.minrangeX, self.maxrangeX, self.step)
        
    def setMinRangeH(self, newmin):
        self.minrangeH = newmin
        self.rangeH = np.arange(self.minrangeH, self.maxrangeH, self.step)
    
    def setMaxRangeX(self, newmax):
        self.maxrangeX = newmax
        self.step = (self.maxrangeX - self.minrangeX)/self.points
        self.rangeX = np.arange(self.minrangeX, self.maxrangeX, self.step)
        
    def setMaxRangeH(self, newmax):
        self.maxrangeH = newmax
        self.rangeH = np.arange(self.minrangeH, self.maxrangeH, self.step)
        
    def setRangeX(self, newmin, newmax):
        self.minrangeX = newmin
        self.maxrangeX = newmax
        self.step = (self.maxrangeX - self.minrangeX)/self.points
        self.rangeX = np.arange(self.minrangeX, self.maxrangeX, self.step)
        
    def setRangeH(self, newmin, newmax):
        self.minrangeH = newmin
        self.maxrangeH = newmax
        self.step = (self.maxrangeH - self.minrangeH)/self.points
        self.rangeH = np.arange(self.minrangeH, self.maxrangeH, self.step)
        
    def setTau(self, tau):
        self.tau = tau
        
    def createEchos(self):
        numberOfEchos = np.floor((self.tau-self.minrangeX)/(self.step*self.echoPoints))
        self.echos = [self.tau - echo*(self.step*self.echoPoints) for echo in np.arange(0,numberOfEchos)]
        print(echos)
        return self.echos
        
        