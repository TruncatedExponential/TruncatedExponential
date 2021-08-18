
# This is the simulation code for the article: 
# A. El-Sayed, H. Al-Mahdi and H. Nassar. “Characterization of task response time in a fog-enabled IoT network using queueing models with general service times,”  Submitted for publication July 2021. 
# The code is made of 5 files as follows:
# main.py:          main file
# MyQueue.py:       Class data type of queue
# VMs.py:           Class data type of virtual machine 
# Sensor.py :       Class data type of terminal device 
# Simulator.py :    Class data type of simulation process

from VMs import virtualMachine
from numpy import random
from MyQueue import queue
from Sensor import Sensor
class Simulator:
	def __init__(self,Lambda=0,mu=0,Taw=0,metric=0,simLength=0,vmNumber=0,populationSize=0, speedFactor=1):
		self.Lambda =Lambda
		self.Taw=Taw
		self.simLength=simLength
		self.FES=[]
		self.vmNumber=vmNumber
		self.populationSize=populationSize
		self.remoteQueue=queue(1000)
		self.localQueue=[]
		for i in range(self.populationSize):
			self.localQueue.append(queue(1000))
		self.vm=[]
		self.CPU=[]
		self.t=0
		self.speedFactor=speedFactor
		self.metric=metric
		self.mu=mu
	def isVmIdle(self):
		for i in range(self.vmNumber):
			v=self.vm[i]
			if v.getState()==0:
				return i,0
		return -1,-1

	def isCPUIdle(self,id):
			cpu=self.CPU[id]
			if cpu.getState()==0:
				return id,0
			return -1,-1

	def setCPUState(self, id, state,t,arrTime,serTime):
		cpu=self.CPU[id]
		cpu.setState(state)
		cpu.setDepartureTime(t)
		cpu.setArrivalTime(arrTime)
		cpu.setServiceTime(serTime)
		self.CPU[id]=cpu

	def idelBusyNumber(self):
		idle=0
		busy=0
		for i in range(self.vmNumber):
			v=self.vm[i]
			if v.getState()==0:
				idle=idle+1
			elif v.getState()==1:
				busy=busy+1
		return idle, busy



	def setVmState(self, id, state,t,arrTime,serTime):
		v=self.vm[id]
		v.setState(state)
		v.setDepartureTime(t)
		v.setArrivalTime(arrTime)
		v.setServiceTime(serTime)
		self.vm[id]=v
        
	def start(self):
		#----------------- For local Buffer ---------------------------------
		for i in range(self.vmNumber):
			self.vm.append(virtualMachine(0,0))

		for i in range(self.populationSize):
			self.CPU.append(virtualMachine(0,0))

		for i in range(self.populationSize):
			arrivalRate=int(random.exponential(scale=(1/self.Lambda)))
			self.FES.append( self.t+arrivalRate)


		while self.t<self.simLength:
		#---------------------- For Arrival scheduing and queueing processes
			for i in range(len(self.FES)):
				if self.FES[i]==self.t:
					nextInterArrivalTime=int(random.exponential(scale=(1/self.Lambda)))
					self.FES[i]=self.t+nextInterArrivalTime
					service=int(random.exponential(scale=(1/self.mu)))
					if service>=self.Taw: # if processing time is greater than Taw then go to the fog queue
						service=int(service/self.speedFactor)
						if service<1:
							service=1
						task=Sensor(self.t,service,0,-1) # 0 : task is not in service , -1 is not associated with any VM
						self.remoteQueue.add(task) # Add task to remote queue
						id,state=self.isVmIdle()  # chech id there is any idle VM
						if state==0: # if VM ide
							s=self.remoteQueue.dequeue()  # get task from the head of the queue
							self.setVmState(id,1,self.t+s.getServiceTime(),s.getArrivalTime(),s.getServiceTime())
					elif service<=self.Taw:
							task=Sensor(self.t,service,0,-1) # 0 : task is not in service , -1 is not associated with any CPU
							self.localQueue[i].add(task) # Add task to local queue of MD i
							id,state=self.isCPUIdle(i)  # check CPU i is idle or not
							if state==0: # if CPU is idle
								s=self.localQueue[i].dequeue()  # get task from the head of the queue
								self.setCPUState(i,1,self.t+s.getServiceTime(),s.getArrivalTime(),s.getServiceTime())
 		#------------------------------------ For Deparure handling from fog --------------------
			for i in range(len(self.vm)):
 				v=self.vm[i] # get VMs from its List one by one
 				if v.getDepartureTime()==self.t and v.getState()==1: # if VM i is busy and it must switch to idle now
 					self.remoteQueue.ClacStatictics(self.t,v.getArrivalTime(),v.getServiceTime()) # Collect statistics
 					v.setState(0)
 					v.setDepartureTime(0)
 					v.setArrivalTime(0)
 					v.setServiceTime(0)
 					self.vm[i]=v
 					# I,B=self.idelBusyNumber()
 					# print("I = ",I, " Busy",B," buffer size  = ",self.remoteQueue.getSize())
 					if self.remoteQueue.getSize()>0:
 						id,state=self.isVmIdle()
 						if state==0:
 							s=self.remoteQueue.dequeue()# Delete the first task from remote queue and return it
 							self.setVmState(id,1,self.t+s.getServiceTime(),s.getArrivalTime(),s.getServiceTime())
#---------------------------------- For depatrure handling at MD -------------------------------------------
			for i in range(len(self.CPU)):
 				cpu=self.CPU[i] # get VMs from its List one by one
 				if cpu.getDepartureTime()==self.t and cpu.getState()==1: # if VM i is busy and it must switch to idle now
 					self.localQueue[i].ClacStatictics(self.t,cpu.getArrivalTime(),cpu.getServiceTime()) # Collect statistics
 					cpu.setState(0)
 					cpu.setDepartureTime(0)
 					cpu.setArrivalTime(0)
 					cpu.setServiceTime(0)
 					self.CPU[i]=cpu

 					if self.localQueue[i].getSize()>0:
 						id,state=self.isCPUIdle(i)
 						if state==0: # if CPU of MD i is idle
 							s=self.localQueue[i].dequeue()	# get task from the head of the queue
 							self.setCPUState(i,1,self.t+s.getServiceTime(),s.getArrivalTime(),s.getServiceTime())
#-----------------------------------------------------------------------------------------------------------
			self.t=self.t+1

#-----------------------------------------------------------------------------------
		if self.metric==1:
			sum=0
			for i in range(self.populationSize):
				sum=sum+self.localQueue[i].getMeanWaitingTime()
			res1=sum/self.populationSize
			res2=self.remoteQueue.getMeanWaitingTime()

			totalTime=0
			totalTask=0
			for i in range(self.populationSize):
				totalTime=totalTime+self.localQueue[i].getallQueueingTime()
				totalTask=totalTask+self.localQueue[i].getNumOfServiedTasks()

			totalTime=totalTime+self.remoteQueue.getallQueueingTime()
			totalTask=totalTask+self.remoteQueue.getNumOfServiedTasks()

			res3=totalTime/totalTask

			return (res1,res2,res3)
		elif self.metric==2:
			sum=0
			for i in range(self.populationSize):
				sum=sum+self.localQueue[i].getMeanSojournTime()
			res1=sum/self.populationSize
			#res1=self.localQueue[0].getMeanSojournTime()
			res2=self.remoteQueue.getMeanSojournTime()

			totalTime=0
			totalTask=0
			for i in range(self.populationSize):
				totalTime=totalTime+self.localQueue[i].getallSystemTime()
				totalTask=totalTask+self.localQueue[i].getNumOfServiedTasks()

			totalTime=totalTime+self.remoteQueue.getallSystemTime()
			totalTask=totalTask+self.remoteQueue.getNumOfServiedTasks()

			res3=totalTime/totalTask

			return (res1,res2,res3)

