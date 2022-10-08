#!/usr/bin/env python3
import json
from pickle import FALSE
from geographiclib.geodesic import Geodesic


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
        self.lon = lon
        self.lat = lat
        self.alt = alt
        self.time = time
        self.fix_type = fix
        self.satellites_visible = satellites
    def __str__(self):
        return "(Lat:" + str(self.lat) + " Lon:" + str(self.lon) + " Altitude:" + str(self.alt) + ")"

class Battery(object):
    """
    voltage: float units V
    current: float units mA
    level: int unitless (0-100)
    m_kg: battery mass, units kg
    """
    def __init__(self):
        self.voltage = float
        self.current = float
        self.level = float
        self.m_kg = float
        
class iperfInfo(object):
    def __init__(self, ipaddr="172.16.0.1", port=5201, protocol="tcp", priority=0, mbps=0, meanrtt=0):
        self.ipaddr = ipaddr #string server ip address
        self.port = port #string server port address 
        self.protocol = protocol #tcp, udp
        self.priority = 1 #normalized float 0-1         
        self.mbps = mbps #float, units mbps, representing throughput
        self.meanrtt = meanrtt #float, units ms, representing latency
        self.location4d = [float, float, float, str]
        
class collectVideoInfo(object):
    def __init__(self, dataformat="jpgframes", duration=5, quality=100, priority = 1):
        self.dataformat = dataformat #jpgframes, ffmpeg, etc
        self.duration = duration #units seconds
        self.quality = quality #arbitrary unit
        self.priority = priority #normalized float 0-1

class sendFrameInfo(object):
    def __init__(self, dataformat="jpgframes", ipaddr="172.16.0.1", port="8096", priority=1):
        self.dataformat = dataformat #jpgframes, ffmpeg, etc
        self.ipaddr = ipaddr #string ip address
        self.port = port #int port number
        self.priority = priority #normalized float 0-1
        
class sendVideoInfo(object):
    def __init__(self, dataformat="jpgframes", ipaddr="172.16.0.1", port="23000", priority=1):
        self.dataformat = dataformat #jpgframes, ffmpeg, etc
        self.ipaddr = ipaddr #string ip address
        self.port = port #int port number 
        self.priority = priority #normalized float 0-1

class flightInfo(object):
    def __init__(self):
        """
        coords : [float,float]--> [lon, lat]
        altitude: float --> M AGL(?)
        airspeed: float --> 
        """
        self.coords = [] #[lon, lat]
        self.altitude = float #meters 
        self.airspeed = float #airspeed 
        self.groundspeed = float #groundspeed
        self.priority = float #normalized float 0-1

class missionInfo(object):
    #we'll have to think this through for different mission types
    def __init__(self):
        self.defaultWaypoints = [] #planfile
        self.tasks = []#tasks associated with each waypoint
        self.missionType = str #videography, delivery, air taxi, etc.
        self.missionLeader = str #basestation, drone, cloud, edge device(s)
        self.priority = float #normalized float from 0-1
        self.planfile = str #path to planfile optional 
        self.name = str #the name of the mission
        self.resources = bool #true-> outside resources/edge devices false-> just drone and basestation
        self.STATUS = str
        self.missionObjectives = []

class MissionObjective(object):
        def __init__(self,way,type,static):
            self.Waypoint = way
            self.Type = type
            self.Static = static

        
class resourceInfo(object):
    def __init__(self):
        self.name = str #identifier for resource
        self.location = str #edge, cloud x, cloud y
        self.purpose = str #mission related I guess
        self.interface = str #thinking something like direct vs kubectl
        self.resourceAddresses = [] #one or more ways to communicate with resource... possibly a pairing? eg ("management", "xxx.xxx.xxx.xxx")
        self.state = str #resource reservation state
        self.load = float #placeholder for now... maybe if we have info from prometheus or something
    
class VehicleCommands(object):#This is like a task?
    def __init__(self):
        self.commands = {}
        self.commands['iperf'] = {}
        self.commands['sendFrame'] = {}
        self.commands['sendVideo'] = {} 
        self.commands['collectVideo'] = {}
        self.commands['flight'] = {}
        
    def setIperfCommand(self, iperfObj):
        self.commands['iperf'] = { "command" : "iperf", "protocol": iperfObj.protocol, "ipaddr": iperfObj.ipaddr, "port": iperfObj.port, "priority": iperfObj.priority } 
    def setCollectVideoCommand(self, collectVideoObj):
        self.commands['collectVideo'] = { "command" : "collectVideo", "dataformat" : collectVideoObj.dataformat, "duration": collectVideoObj.duration, "quality": collectVideoObj.quality, "priority": collectVideoObj.priority }
    def setSendFrameCommand(self, sendFrameObj):
        self.commands['sendFrame'] = { "command" : "sendFrame", "dataformat" : sendFrameObj.dataformat, "ipaddr": sendFrameObj.ipaddr, "port": sendFrameObj.port, "priority": sendFrameObj.priority  }
    def setSendVideoCommand(self, sendVideoObj):
        self.commands['sendVideo'] = { "command" : "sendVideo", "dataformat" : sendVideoObj.dataformat, "ipaddr": sendVideoObj.ipaddr, "port": sendVideoObj.port, "priority": sendVideoObj.priority  }
    def setFlightCommand(self, flightObj):
        self.commands['flight'] = { "command" : "flight", "destination" : flightObj.destination, "speed": flightObj.speed, "priority": flightObj.priority }
    def setMissionCommand(self, missionObj):
        self.commands['mission'] = { "command": "mission", "defaultWaypoints": missionObj.defaultWaypoints, "missionType": missionObj.missionType, "missionControl": missionObj.missionControl, "priority": missionObj.priority }

class droneSim(object):
    def __init__(self):
        self.position = Position()
        self.nextWaypoint = []
        self.battery = Battery()
        self.heading = float
        self.home = []


class taskedWaypoint(object):
    def __init__(self):
        self.position = Position()
        self.task = str
        self.TimeSensitive = bool

class Task(object):
    def __init__(self, pos,task,sensitive,prio):
        self.position = pos
        self.task = task
        self.TimeSensitive = sensitive
        self.priority = prio
        self.comms_required = False
        self.dynamicTask = False

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
        if self.Empty():
            print("Empty!")
        else:
            print("")
            print("============")
            print("====TOP\u2193 ===")
            for idx, task in enumerate(self.queue):
                if(task.dynamicTask):
                    print("|D"+str(task.task).rjust(10,"+")+"|")
                else:
                    print("|"+str(task.task).rjust(10," ")+"|")
                #print("Task#: "+str(idx)+" Lat:"+ str(task.position.lat)+ " Lon:"+ str(task.position.lon)+" Alt:"+ str(task.position.alt) )
            print("===BOTTOM===")
            print("============")
            print("Count: "+ str(self.Count))
            print("Next Task: " + str(task.task) + ": Postion-- Lat:"+ str(task.position.lat)+ " Lon:"+ str(task.position.lon)+" Alt:"+ str(task.position.alt))
            print("")
    def Empty(self):
        if(self.Count == 0):
            return True
        elif(self.Count>0): 
            return False

    def NextTask(self):
        if not self.Empty():
            return self.queue[self.Count-1]
        else:
            return False
    def AppendTask(self,task):
        self.queue.append(task)
        self.Count =  self.Count + 1

            




class RadioMap(object):
    def __init__(self):
        self.lats = []
        self.lons = []
        self.headings = []
        self.dataRate = []
        self.length = 0
        self.positions =[]
    def Add(self, lat, lon, heading, rate):
        self.lats.append(lat)
        self.lons.append(lon)
        self.headings.append(heading)
        self.dataRate.append(rate)
        self.length = self.length + 1
        pos = Position()
        pos.InitParams(lon,lat,0,0,0,0)
        self.positions.append(pos)


    def FindClosestPointWithConnection(self,nextPoint,currentPosition,radioPosition):
        geo = Geodesic.WGS84.Inverse(currentPosition.lat, currentPosition.lon, radioPosition.lat, radioPosition.lon)
        distance_to_base = geo.get('s12')
        minFlightDistance = distance_to_base
        suggestedPositon = radioPosition

        for idx, position in enumerate(self.positions) :
            if(self.dataRate[idx]>0):

                geo = Geodesic.WGS84.Inverse(currentPosition.lat, currentPosition.lon, position.lat, position.lon)
                distance_to_drone = geo.get('s12')
                if minFlightDistance>distance_to_drone :
                    minFlightDistance = distance_to_drone
                    suggestedPositon = position
            

        return suggestedPositon
        