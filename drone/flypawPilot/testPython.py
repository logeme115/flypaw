from turtle import position


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

class Task(object):
    def __init__(self, pos,task,sensitive,prio):
        self.position = pos
        self.task = task
        self.TimeSensitive = sensitive
        self.priority = prio

class TaskQueue(object):

    def __init__(self):
        self.queue = []
        self.Count = 0
    def PushTask(self, task:Task):
        self.queue.insert(0,task)
        self.Count =  self.Count + 1
    def PopTask(self):
        if(self.queue):
            self.Count = self.Count-1 #Adjust count
            return self.queue.pop(self.Count)#Pop item at end of queue
    def PrintQ(self):#change this to lower case please
        if len(self.queue) < 1:
            print("Empty!")
        else:
            for idx, task in enumerate(self.queue):
                print("Task#: "+str(idx)+" Lat:"+ str(task.position.lat)+ " Lon:"+ str(task.position.lon)+" Alt:"+ str(task.position.alt) )




class Position(object):
    """
    lon: float units degrees (-180..180)
    lat: float units degrees (-90..90)
    alt: float units M AGL
    time: str, iso8601 currently
    fix_type: int (0..4), 0-1 = no fix, 2 = 2D fix, 3 = 3D fix
    satellites_visible: int (0..?)
    """
    def __init__(self):
        self.lon = float
        self.lat = float
        self.alt = float
        self.time = str
        self.fix_type = int
        self.satellites_visible = int
    def InitParams(self,lon,lat,alt,time,fix,satellites):
        self.lon = float
        self.lat = float
        self.alt = float
        self.time = str
        self.fix_type = int
        self.satellites_visible = int

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
p = Position()
p.InitParams(1,2,3,4,5,6)
t = Task(p,0,0,0)
tq = TaskQueue()
print("tq: "+ str(bool(tq)))
tq.PrintQ()
tq.PushTask(t)
tq.PrintQ()
print("tq: "+ str(bool(tq)))


