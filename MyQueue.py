# This is the simulation code for the article: 
# A. El-Sayed, H. Al-Mahdi and H. Nassar. “Characterization of task response time in a fog-enabled IoT network using queueing models with general service times,”  Submitted for publication July 2021. 
# The code is made of 5 files as follows:
# main.py:          main file
# MyQueue.py:       Class data type of queue
# VMs.py:           Class data type of virtual machine 
# Sensor.py :       Class data type of terminal device 
# Simulator.py :    Class data type of simulation process

class queue:
	def __init__(self,maxSize=0):
		self.maxSize =maxSize
		self.buffer=[]
		self.sumW = 0;
		self.sumW2 = 0;
		self.sumS = 0;
		self.sumS2 = 0;
		self.n = 0;
		self.surface = 0;
		self.t = 0;
		self.timeCPUBusy=0
		self.timeBlock=0;
		self.surfaceBlock=0;
	def setSize(self,s):
		self.maxSize=s
	def getSize(self):
		return len(self.buffer)

	def add(self,sensor):
		size=len(self.buffer)
		currentTime = sensor.getArrivalTime();
		if currentTime <self.t:
			print("Negeative 1")
		self.surface+=(size*(currentTime - self.t))
		self.t=currentTime
		self.buffer.append(sensor)

	def enterService(self,ID):
		for i in range(len(self.buffer)):
			task=self.buffer[i]
			if task.getinServices()==0 and task.getVmID()==-1:
				task.setinServices(1)
				task.setVmID(ID)
				self.buffer[i]=task
				break

	def dequeue(self):
		s=self.buffer.pop(0)
		return s

	def ClacStatictics(self,currentTime,arrivalTime,serviceTime):
		size = len(self.buffer)+1
		if currentTime < arrivalTime:
			print("Negeative 2")
		self.sumS+= currentTime - arrivalTime
		self.sumS2+= (currentTime-arrivalTime) * (currentTime - arrivalTime)
		self.sumW += currentTime-arrivalTime-serviceTime
		if (currentTime-arrivalTime-serviceTime) < 0:
			print("Negeative 3")
		self.sumW2+= (currentTime - arrivalTime - serviceTime) * (currentTime - arrivalTime - serviceTime)
		self.n+=1
		self.timeCPUBusy+=serviceTime
		self.surface += size * (currentTime - self.t)
		self.t=currentTime


	def getSensorAtHead(self,vmID):
		for i in range(len(self.buffer)):
			task=self.buffer[i]
			if task.getinServices()==0 and task.getVmID()==-1:
				task.setinServices(1)
				task.setVmID=vmID
				self.buffer[i]=task
				return task.getServiceTime()

		return -1

	def bufferBlock(self,currentTime):
		self.surfaceBlock+=currentTime

	def getsurfaceBlock(self):
		return self.surfaceBlock
	def getBlock(self,tt):
		return	self.surfaceBlock/tt

	def getMeanWaitingTime(self): # task waiting time in queue
		if self.n==0:
			return 0
		else:
			return self.sumW / self.n
	def getMeanSojournTime(self): # response time
		if self.n==0:
			return 0
		else:
			return self.sumS / self.n
	def getMeanNumberOfSensors(self):
		return self.surface/self.t
	def getUtilization(self):  # CPU utilization
		return self.timeCPUBusy/self.t
	def getThroughput(self,mu): # System throughput
		return (self.timeCPUBusy/self.t)*mu
	def getallSystemTime(self): # System throughput
		return self.sumS
	def getNumOfServiedTasks(self): # System throughput
		return self.n
	def getallQueueingTime(self): # System throughput
		return self.sumW



