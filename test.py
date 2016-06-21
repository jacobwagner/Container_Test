from dataContract.containerInfo import ContainerInfo
from cmd.lxcCommandWrap import LXC
from dataContract.containerState import ContainerState
from dataContract.serviceName import ServiceName
from dataContract.serviceStatus import ServiceStatus
from dataContract.containerType import ContainerType
import time
import random
import sys


##sc = Service()
##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
##sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Stop)
##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
##sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Start)
##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)

containerInfo = ContainerInfo()

def generateList():
	try:
		stopList = []
		runningList = []
		containerList = containerInfo.getAllContainerList()
		for i in containerList:
			if i.getState() == "RUNNING":
				runningList.append(i.getName())
			elif i.getState() == "STOPPED":
				stopList.append(i.getName())
		return runningList, stopList
	except:
		print "generateList error"
		return [], []
		
def randomTest(minimumTime, MaximumTime):
	l = LXC()
	while 1:
		try:
			runningList, stopList = generateList()
			ran = random.randint(0, 1)
			#try get one randome container from running list then stop it
			if ran == 1:
				index = getRandomInt(len(runningList))
				if index != -1:
					print "about to stop: " + runningList[index] 
					l.stop(runningList[index])
				else:
					print "doing nothing"
			else:
				index = getRandomInt(len(stopList))
				if index != -1:
					print "about to start: " + runningList[index] 
					l.start(stopList[index])
				else:
					print "doing nothing"
			t = getRandomInt(MaximumTime-minimumTime)+minimumTime
			print 'Sleep for %s seconds' %  str(t)
			time.sleep(t)
		except KeyboardInterrupt:
			sys.exit(0)
		except:
			print "shit happened"
			sys.exit(0)

def getRandomInt(num):
	if num > 0:
		return random.randint(0,num-1)
	else:
		return -1 

randomTest(30, 50)
