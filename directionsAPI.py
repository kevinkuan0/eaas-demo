import json
import urllib2
from decode import decode

class DirAPI:

    def __init__(self,
                 jpath = 'C:/Users/Kevin/Desktop/EaaS/GoogleMap/HtoY_M/HtoY_M_Dir.json'):
        self.j = None
        self.jpath = jpath   
        self.rlen = 0
        self.slen = []

    def routes(self):
        if self.j is None: return None
        return self.j['routes']
        
    def steps(self, rid):
        if self.j is None: return None
        return self.j['routes'][rid]['legs'][0]['steps']

    def get_new_json(self,
                     origin = (24.841443,121.015447),
                     destination = (24.705530,121.739171),
                     avoid_highways = True,
                     alternatives = False):
                         
        self.origin = origin
        self.destination = destination
        self.avoid_highways = avoid_highways
        self.alternatives = alternatives

        query = "https://maps.googleapis.com/maps/api/directions/json"
        query += "?key=AIzaSyA_tnq2piP_G_XFn0ETq_UGA3yWYVoetf8"
        query += "&origin=%f,%f" % self.origin
        query += "&destination=%f,%f" % self.destination
        if self.avoid_highways: 
            query += "&avoid=highways"
        if self.alternatives:
            query += "&alternatives=false"
        
        u = urllib2.urlopen(query).read()
        self.j = json.loads(u)
        with open(self.jpath, 'w') as f:
            json.dump(self.j, f)

        self.rlen = len(self.j['routes'])
        self.slen = [len(self.steps(rid)) for rid in range(self.rlen)]
    
    def load_old_json(self):
        with open( self.jpath, 'r') as f:
            self.j = json.load(f)
        self.rlen = len(self.j['routes'])
        self.slen = [len(self.steps(rid)) for rid in range(self.rlen)]

    
    def print_csv(self, rid):
        print 'HtoY_M%d' % rid
        s = ''
        ss = self.steps(rid)
        for sid in range(len(ss)):
            sss = ss[sid]
            slat = '%f %f' % (sss['start_location']['lat'] , sss['start_location']['lng'])
            elat = '%f %f' % (sss['end_location']['lat'] , sss['start_location']['lng'])
            d = float(sss['distance']['value'])
            t = float(sss['duration']['value'])
            
            s += '%f,%s,%s,%f,%f,%f,%f,%f,%f,%f,%f\n' % (
                    sid, slat, elat, d, 0, 0, 0, 0, t, d/t, d/t * 3.6)
            print sid, slat, elat, d, 0, 0, 0, 0, t, d/t, d/t * 3.6
        return s
    
    def save_dir_csv(self, f):
        f.write('RouteID,SegmentID,Distance,Duration\n')
        
        for rid in range(len(self.j['routes'])):
            ss = self.steps(rid)
            for sid in range(len(ss)):
                sss = ss[sid]
                d = float(sss['distance']['value'])
                t = float(sss['duration']['value'])
                f.write('%d,%d,%f,%f\n' % (rid,sid,d,t))
        
    def save_point_csv(self, f):
        f.write('RouteID,SegmentID,PointID,latitude,longitude\n')
        for rid in range(len(self.j['routes'])):
            ss = self.steps(rid)
            for sid in range(len(ss)):
                sss = ss[sid]
                polyline = decode(sss['polyline']['points'])
                latlngs = [(p[1], p[0]) for p in polyline[0:50]]
                for pid in range(len(latlngs)):
                    f.write('%d,%d,%d,%f,%f\n' % (rid, sid, pid) + latlngs[pid])

    def save_path_csv(self, f):
        f.write('RouteID,SegmentID,PointID,latlng1,latlng2\n')
        for rid in range(len(self.j['routes'])):
            ss = self.steps(rid)
            for sid in range(len(ss)):
                sss = ss[sid]
                polyline = decode(sss['polyline']['points'])
                latlngs = ['%fx%f' % (p[1], p[0]) for p in polyline[0:50]]
                for pid in range(len(latlngs) - 1):
                    f.write('%d,%d,%d,%s,%s\n' % (rid, sid, pid, latlngs[pid], latlngs[pid+1]))

    
    def print_path(self, rid):
        steps = self.steps(rid)
        path = ['%(lat)f,%(lng)f' % s['start_location'] for s in steps]
        path.append('%(lat)f,%(lng)f' % (steps[-1]['end_location']))
        print '|'.join(path)
        return '|'.join(path)
        
    