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
        self.minrange = 0
        self.maxrange = 10
        self.points = 1000
        self.step = (self.maxrange - self.minrange)/self.points
        self.range = np.linspace(self.minrange, self.maxrange, self.points)
        
    def getMinRange(self):
        return self.minrange
    
    def getMaxRange(self):
        return self.maxrange
    
    def getStep(self):
        return self.step
        
    def getXfunction(self):
        self.x = np.sin(self.range*np.pi)
        return [self.range, self.x]
    
    def getHfunction(self):
        self.h = np.exp(-self.range)
        return [self.range, self.h]
    
    def getConvolution(self):
        self.result = np.convolve(self.x, self.h)
        self.convolveRange = np.linspace(self.minrange, self.minrange+(self.result.size*self.step), num=self.result.size)
        return [self.convolveRange, self.result]


    def setMinRange(self, newmin):
        self.minrange = newmin
        self.range = np.linspace(self.minrange, self.maxrange, self.points)
    
    def setMaxRange(self, newmax):
        self.maxrange = newmax
        self.range = np.linspace(self.minrange, self.maxrange, self.points)
        
    def setRange(self, newmin, newmax):
        self.minrange = newmin
        self.maxrange = newmax
        self.range = np.linspace(self.minrange, self.maxrange, self.points)