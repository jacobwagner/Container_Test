from dataContract.containerInfo import ContainerInfo
from cmd.lxcCommandWrap import LXC
from dataContract.containerState import ContainerState
from dataContract.serviceName import ServiceName
from dataContract.serviceStatus import ServiceStatus
from dataContract.containerType import ContainerType
from log import logging
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
logger = logging.getLogger('ContainerControl')

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
		logger.info("generateList error")
		return [], []
		
def randomTest(minimumTime, MaximumTime):
	logger.info("Starting chaos...")
	l = LXC()
	while 1:
		try:
			runningList, stopList = generateList()
			ran = random.randint(0, 1)
			t = getRandomInt(MaximumTime-minimumTime)+minimumTime
			#try get one randome container from running list then stop it
			if ran == 1:
				index = getRandomInt(len(runningList))
				if index != -1:
					logger.info("about to stop: " + runningList[index])
					l.stop(runningList[index])
				else:
					logger.info("Doing nothing for the next %s seconds" % str(t))
			else:
				index = getRandomInt(len(stopList))
				if index != -1:
					logger.info("about to start: " + runningList[index])
					l.start(stopList[index])
				else:
					logger.info("Doing nothing for the next %s seconds" % str(t))
			countDown(t)
		except KeyboardInterrupt:
			logger.info("Stoping chaos...")
			sys.exit(0)
		except:
			print "shit happened"
			sys.exit(0)

def getRandomInt(num):
	if num > 0:
		return random.randint(0,num-1)
	else:
		return -1 

def countDown(t):
	if t > 0:
		for i in xrange(t-1, 0, -1):
			logger.info('Sleep for %s seconds' %  str(i))
			sys.stdout.flush()
			time.sleep(1)	

randomTest(5, 10)
