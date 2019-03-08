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
        self.step = 0.01
        self.range = np.arange(self.minrange, self.maxrange, self.step)
        
    def getXfunction(self):
        x = np.sin(self.range*np.pi)
        return [self.range, x]
    
    def getHfunction(self):
        x = np.exp(-self.range)
        return [self.range, x]
