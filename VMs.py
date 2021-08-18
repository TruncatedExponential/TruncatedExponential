# This is the simulation code for the article: 
# A. El-Sayed, H. Al-Mahdi and H. Nassar. “Characterization of task response time in a fog-enabled IoT network using queueing models with general service times,”  Submitted for publication July 2021. 
# The code is made of 5 files as follows:
# main.py:          main file
# MyQueue.py:       Class data type of queue
# VMs.py:           Class data type of virtual machine 
# Sensor.py :       Class data type of terminal device 
# Simulator.py :    Class data type of simulation process

class virtualMachine():
    def __init__(self,state=0,t=0,arr=0,ser=0):
        self.state = state
        self.departureTime=t
        self.arrivalTime=arr
        self.serviceTime=ser

    def setState(self,state):
        self.state=state

    def getState(self):
        return self.state
    def setDepartureTime(self,departureTime):
        self.departureTime=departureTime

    def getDepartureTime(self):
        return self.departureTime

    def setArrivalTime(self,arri):
        self.arrivalTime=arri
    def getArrivalTime(self):
        return self.arrivalTime

    def setServiceTime(self,serv):
        self.serviceTime=serv
    def getServiceTime(self):
        return self.serviceTime


