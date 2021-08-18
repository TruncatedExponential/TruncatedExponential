# This is the simulation code for the article: 
# A. El-Sayed, H. Al-Mahdi and H. Nassar. “Characterization of task response time in a fog-enabled IoT network using queueing models with general service times,”  Submitted for publication July 2021. 
# The code is made of 5 files as follows:
# main.py:          main file
# MyQueue.py:       Class data type of queue
# VMs.py:           Class data type of virtual machine 
# Sensor.py :       Class data type of terminal device 
# Simulator.py :    Class data type of simulation process

from Simulator import Simulator
import math
from datetime import datetime
#----------------- Simulation parameters ------------------------
speedFactor=10
C=5
N=500
Lambda=0.000001  #1/7200  #Arrival Rate
step=0.000009
mu=1/900 	# For data size ditribution
Taw=500	#Truncation parameter
e=math.exp(-mu*Taw) 			#e=e^(-Segma*Taw)
Alpha=1-e

#------------------------ Simulation time ---------------------------
simlen=20000
#------------------------------------------------------------------------------
metric =2  # For claculating Sojourn Time
#---------------------------------------------------------------------
choice = input('''Choose the varying parameter of the experiment: 
               1. The number of VMs (C).
               2. The off-loading thresohld (Taw).
               3. The number of terminal devices (N).
               4. The arrival rate of processes (Lambda).
               5. Speed-up factor (K).
               6. The task processing time Mu
               Your Choice is ''')
print('Simulation Started at', datetime.now().strftime("%H:%M:%S"))

if choice=='1':
#--------------------- For varing C -----------------------------
    print("N (MDs) = ",N," Taw = ",Taw,"Speed = ",speedFactor,"Lambda = ",Lambda," mu = ",mu," Alpha = ",Alpha)
    C=2
    while C<=9:
        sim=Simulator(Lambda,mu,Taw,metric,simlen,C,N,speedFactor)
        (result1,result2,result3)=sim.start()
        print("(",C,",",result1,",",result2,",",result3,")")
        C+=1
elif choice=='2':        
#--------------------- For varing Taw -----------------------------
    print("N (MDs) = ",N," Taw = ",Taw,"Speed = ",speedFactor,"Lambda = ",Lambda," C = ",C," Alpha = ",Alpha)
    while mu<=0.01:
        sim=Simulator(Lambda,mu,Taw,metric,simlen,C,N,speedFactor)
        (result1,result2,result3)=sim.start()    
        print("(",mu,",",result1,",",result2,",",result3,")")
        mu+=0.001
#--------------------- For varing N -----------------------------
elif choice=='3':    
    print("Taw ",Taw," C (VMs) = ",C,"Speed = ",speedFactor,"Lambda = ",Lambda," mu = ",mu," Alpha = ",Alpha)
    N=100
    while N<=500:
        sim=Simulator(Lambda,mu,Taw,metric,simlen,C,N,speedFactor)
        (result1,result2,result3)=sim.start()
        print("(",N,",",result1,",",result2,",",result3,")")
        N+=100
#----------------- For Varing Lambda  -----------------------------------------------
elif choice=='4':    
    print("N (MDs) = ",N," C (VMs) = ",C,"Speed = ",speedFactor,"Lambda = ",Lambda," mu = ",mu," Alpha = ",Alpha)
    while Lambda<=6.400000000000001e-05:
        sim=Simulator(Lambda,mu,Taw,metric,simlen,C,N,speedFactor)
        (result1,result2,result3)=sim.start()
        print("(",Lambda,",",result1,",",result2,",",result3,")")
        Lambda+=step
elif choice=='5':   
#----------------- For Varing k  -----------------------------------------------
    print("N (MDs) = ",N," C (VMs) = ",C,"Speed = ",speedFactor,"Lambda = ",Lambda," mu = ",mu," Alpha = ",Alpha)
    speedFactor=2
    while speedFactor<=40:
        sim=Simulator(Lambda,mu,Taw,metric,simlen,C,N,speedFactor)
        (result1,result2,result3)=sim.start()
        print("(",speedFactor,",",result1,",",result2,",",result3,")")
        speedFactor+=2
#--------------------------- For Varing taw  -------------------------------------------
elif choice=='6':   
    print("N (MDs) = ",N," C (VMs) = ",C,"Speed = ",speedFactor,"Lambda = ",Lambda," mu = ",mu,)
    Taw=200
    while Taw<=5000:
        sim=Simulator(Lambda,mu,Taw,metric,simlen,C,N,speedFactor)
        (result1,result2,result3)=sim.start()    
        Taw+=200
        e=math.exp(-mu*Taw)             #e=e^(-Segma*Taw)
        Alpha=1-e
#-------------------------------------------------------------------------------------
#----------------------------------------------------------------------------
print('Simulation Ended at', datetime.now().strftime("%H:%M:%S"))