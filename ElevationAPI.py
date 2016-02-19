# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:30:20 2016

@author: Kevin
"""
import json
import urllib2
from math import atan2
from geopy.distance import distance

class ElevationAPI:
    
    def __init__(self,
                 jpath = 'C:/Users/Kevin/Desktop/EaaS/GoogleMap/HtoY_M/HtoY_M_Elev.json',
                 ):
        self.j = None
        self.jpath = jpath
        self.str = None
        

    def points(self):
        if self.j is None: return None
        return self.j['results']
    
    def lat(self, i):
        if self.j is None: 
            return None
        else:
            return self.j['results'][i]['location']['lat']
        
    def lng(self, i):
        if self.j is None: 
            return None
        else:
            return self.j['results'][i]['location']['lng']
    
    def latlng(self, i):
        if self.j is None: return None
        return ( self.lat(i), self.lng(i) )
        
    
        
    def elev(self, i):
        if self.j is None: return None
        return self.j['results'][i]['elevation']
        
    def res(self, i):
        if self.j is None: return None
        return self.j['results'][i]['resolution']

    def get_new_json(self,
                     path = '36.578581,-118.291994|36.23998,-116.83171',
                     samples = 3):
        self.path = path
        self.samples = samples
        
        query = "https://maps.googleapis.com/maps/api/elevation/json"
        query += "?key=AIzaSyA_tnq2piP_G_XFn0ETq_UGA3yWYVoetf8"
        query += "&path=" + self.path
        query += "&samples=%d" % self.samples

        self.str = urllib2.urlopen(query).read()
        self.j = json.loads(self.str)
        
        with open(self.jpath, 'w') as f:
            json.dump(self.j, f)
            
    def load_old_json(self):
        with open( self.jpath, 'r') as f:
            self.j = json.load(f)
            
    def _flatten(self, p):
        return (p['elevation'], p['location']['lat'], p['location']['lng'], p['resolution'])

    def print_point_csv_(self):
        print 'elevation', 'lat', 'lng', 'resolution'
        s = 'elevation,lat,lng,resolution\n'
        for p in self.j['results']:
            f = self._flatten(p)
            print f[0], f[1], f[2], f[3]
            s += '%f,%f,%f,%f\n' % f
        return s
    
    def print_csv(self):
        print 'elev1, lat1, lng1, res1, elev2, lat2, lng2, res2, d(m)'
        s = 'elev1,lat1,lng1,res1,elev2,lat2,lng2,res2,d(m)\n'
        r = self.j['results']
        for i in range(len(r) - 1):
            (f1, f2) = (self._flatten(r[i]), self._flatten(r[i+1]))
            d = distance((f1[1], f1[2]), (f2[1], f2[2]))
            print f1, f2, d.m
            s += '%f,%f,%f,%f,%f,%f,%f,%f,%f\n' % (f1 + f2 + tuple([d.m]))
        return s
        
    def save_elev_csv(self, f):
        f.write('EPointID,Latitude,Longitude,Elevation,Resolution\n')
        for rid in range(len(self.j['results'])):
            r = self.j['results'][rid]
            f.write('%d,%f,%f,%f' % (rid, 
                                     r['location']['lat'], 
                                     r['location']['lng'], 
                                     r['elevation'],
                                     r['resolution']) )
            
    def print_path(self):
        path = ['%(lat)f,%(lng)f' % r['location'] for r in self.j['results']]
        print '|'.join(path)
        return '|'.join(path)
        
    def print_path2(self):
        path = ['{lat:%(lat)f,lng:%(lng)f}' % r['location'] for r in self.j['results']]
        print ','.join(path)
        return ','.join(path)