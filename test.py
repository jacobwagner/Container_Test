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
import re


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
				runningList.append(i)
			elif i.getState() == "STOPPED":
				stopList.append(i)

		runningList = checkContainerStopable(runningList)

		return runningList, stopList
	except:
		logger.info("generateList error")
		return [], []

def getShortName(name, containerPrefix):
	try:
		if len(name) > 0:
			n = re.split('_container-', name.replace(containerPrefix+'_', ''))[0]
			if 'nova' in n:
				if 'nova_api_os_compute' not in n:
					return 'nova'
			return n
				
	except Exception as inst:
		print "shit"
		logger.info(type(inst))     # the exception instance
		logger.info(inst.args)      # arguments stored in .args
		return ''

def checkContainerStopable(runningList):
	containerPrefix = containerInfo.getContainerPrefix()
	try:
		runningDic = generateDic(runningList, containerPrefix)

		for i in runningDic.viewkeys():
			if runningDic[i] == 1:
				for item in runningList:
					if i in item.getName():
						runningList.remove(item)
		return runningList

	except Exception as inst:
		logger.info(type(inst))     # the exception instance
		logger.info(inst.args)      # arguments stored in .args
		logger.info(inst)   

def generateDic(containerList, containerPrefix):
	dic = {}
	try:
		for item in containerList:
				name = item.getName()
				short = getShortName(name, containerPrefix)
				if short not in dic:
					dic[short] = 1
				else:
					dic[short] += 1
	except Exception as inst:
		logger.info(type(inst))     # the exception instance
		logger.info(inst.args)      # arguments stored in .args
		logger.info(inst)   
	return dic
		
def randomTest(minimumTime, MaximumTime):
	logger.info("Starting chaos...")
	logger.info(time.ctime())
	l = LXC()

	while 1:
		try:
			runningList, stopList = generateList()
			ran = random.randint(0, 1)
			t = getRandomInt(MaximumTime-minimumTime)+minimumTime
			#try get one randome container from running list then stop it
			if ran == 1:
				if len(stopList) > 10:
					continue
				index = getRandomInt(len(runningList))
				if index != -1:
					logger.info("about to stop: " + runningList[index].getName())
					l.stop(runningList[index].getName())
				else:
					logger.info("Doing nothing for the next %s seconds" % str(t))
			else:
				index = getRandomInt(len(stopList))
				if index != -1:
					logger.info("about to start: " + stopList[index].getName())
					l.start(stopList[index].getName())
				else:
					logger.info("Doing nothing for the next %s seconds" % str(t))
			countDown(t)
		except KeyboardInterrupt:
			logger.info("Stoping chaos...")
			sys.exit(0)
		except Exception as inst:
			logger.info(type(inst))     # the exception instance
			logger.info(inst.args)      # arguments stored in .args
			logger.info(inst)   
			logger.info(time.ctime())

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

randomTest(20, 40)
