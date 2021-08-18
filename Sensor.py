# This is the simulation code for the article: 
# A. El-Sayed, H. Al-Mahdi and H. Nassar. “Characterization of task response time in a fog-enabled IoT network using queueing models with general service times,”  Submitted for publication July 2021. 
# The code is made of 5 files as follows:
# main.py:          main file
# MyQueue.py:       Class data type of queue
# VMs.py:           Class data type of virtual machine 
# Sensor.py :       Class data type of terminal device 
# Simulator.py :    Class data type of simulation process

class Sensor:
	 'Class Structure for Sensor'
	 ' Constructor with zero or multiple parameter'
	 def __init__(self,arrivalTime=0,serviceTime=0,inService=0,vmID=-1):
			self.arrivalTime=arrivalTime
			self.serviceTime=serviceTime
			self.inService=inService
			self.vmID=vmID
			'Function to set sensor information'
	 def __str__(self):
		  return 'Sensor id {self.id} type{self.type} datatype {self.datatype} data {self.data} '.format(self=self)
	 def setArrivalTime(self,t):
			self.arrivalTime=t

	 def  setServiceTime(self,t):
			self.serviceTime=t

	 def setinServices(self,status):
			self.inService=status

	 def setVmID(self,ID):
			self.vmID=ID

	 def getArrivalTime(self):
			return self.arrivalTime

	 def getServiceTime(self):
			return self.serviceTime

	 def getinServices(self):
			return self.inService

	 def getVmID(self):
			return self.vmID
