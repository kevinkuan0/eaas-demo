# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 13:10:18 2016

@author: CGGM-kevinkuan0
"""
from untitled0 import getDSVFile
from subprocess import call

def getJDWE():
    with open('file.out') as f:
        line = f.readline()
        return map(float, line.split(' '))
    
def getAll(lat1, lng1, lat2, lng2, avdHigh):
    getDSVFile(lat1, lng1, lat2, lng2, avdHigh)
    call('EV.cmd', shell=True)
    (energy_j, distance, energy_kwh, efficiency) = getJDWE()