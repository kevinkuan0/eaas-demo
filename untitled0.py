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

d = DirAPI()
#d.load_old_json()
#d.get_new_json(avoid_highways=False)
d.get_new_json(
#    origin=(,), 
    destination=(25.072589, 121.557445),
    avoid_highways=False,
    alternatives=False)
    
sample_distance = 100

f = open('emer', 'w')
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