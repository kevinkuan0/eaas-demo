# -*- coding: utf-8 -*-
"""
Created on Fri Feb 05 19:29:12 2016

@author: Kevin
"""

from directionsAPI import DirAPI
from ElevationAPI import ElevationAPI
from decode import decode
from geopy.distance import vincenty
from math import floor, atan2
from subprocess import call

def getDSVFile(lat1, lng1, lat2, lng2, avdHigh):
    d = DirAPI()
    #d.load_old_json()
    #d.get_new_json(avoid_highways=False)
    d.get_new_json(
        origin=(lat1,lng1), 
        destination=(lat2, lng2),
        avoid_highways=avdHigh,
        alternatives=False)
        
    sample_distance = 100
    
    f = open('file', 'w')
    #f2 = open('highway_100_height', 'w')
    #f2.write('SegmentID,Segment2ID,EPointID,latitude,longitude,elevtaion,resolution\n')
    
    #for step in d.steps(0):
    for sid in range(len(d.steps(0))):
        step = d.steps(0)[sid]
    
        velocity = float(step['distance']['value']) / float(step['duration']['value'])
        path_ = decode(step['polyline']['points'])
        path_ = [(p[1], p[0]) for p in path_]
        spath_ = ['%f,%f' % p for p in path_]
        
        for i in range(0, len(path_), 50):
            i2 = min(len(path_), i+50)
            path = path_[i:i2]
            distance = [vincenty(path[j], path[j+1]).m for j in range(len(path) - 1)]
            mileage = sum(distance)
            
            if mileage < sample_distance: break
            samples = int(floor(mileage / sample_distance) + 1)
            
            e = ElevationAPI()
            e.get_new_json(path = '|'.join(spath_[i:i2]), samples = samples)
            
            assert len(e.points()) == samples   
            
            e_distance = [vincenty(e.latlng(ei), e.latlng(ei+1)).m for ei in range(samples-1)]
            e_height = [e.elev(ei) - e.elev(ei+1) for ei in range(samples-1)]
            e_slope = [atan2(e_height[ei], e_distance[ei]) for ei in range(samples-1)]
            
            for ei in range(samples - 1):
                f.write('%d\t%f\t%f\n' % (e_distance[ei], e_slope[ei], velocity))
    #            f.flush()
    
    #        for ei in range(samples):
    #            f2.write('%d,%d,%d,%f,%f,%f,%f\n' % (sid, i, ei, e.lat(ei), e.lng(ei), e.elev(ei), e.res(ei)))
    #            print '%d\t%f\t%f\n' % (e_distance[ei], e_slope[ei], velocity)
    
    f.close()
    #f2.close()
    
def getJDWE():
    with open('file.out') as f:
        line = f.readline()
        return map(float, line.split(' '))
    
def getAll(lat1, lng1, lat2, lng2, avdHigh):
    getDSVFile(lat1, lng1, lat2, lng2, avdHigh)
    call('EV.cmd', shell=True)
    (energy_j, distance, energy_kwh, efficiency) = getJDWE()
    print 'energy_j %f distance %f energy_kwh %f efficiency %f' % (energy_j, distance, energy_kwh, efficiency)
    
if __name__ == "__main__":
    getAll(24.841443,121.015447,24.705530,121.739171,False)