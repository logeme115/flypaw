class RadioMap(object):
    def __init__(self):
        self.lats = []
        self.lons = []
        self.headings = []
        self.dataRate = []
        self.length = 0
    def add(self, lat, lon, heading, rate):
        self.lats.append(lat)
        self.lons.append(lon)
        self.headings.append(heading)
        self.dataRate.append(rate)
        self.length = self.length + 1

def runIperf():

        msg = {}
        msg['uuid'] = str(5)
        msg['type'] = "iperfResults"
        msg['iperfResults'] = {}










        msg['iperfResults']['protocol'] = "tcp"
        msg['iperfResults']['location4d'] = [ 1,2,3,4 ]
        msg['iperfResults']['heading'] = [ 33 ]


        return msg

a = RadioMap()
a.add(1,2,3,4)
a.add(4,3,2,1)
print(a.lons)
ret  = runIperf()
print(ret.uuid)

