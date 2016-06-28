from dataContract.infoParser import InfoParser 
from cmd.lxcCommandWrap import LXC
from dataContract.containerState import ContainerState
from dataContract.serviceName import ServiceName
from dataContract.serviceStatus import ServiceStatus
from dataContract.containerType import ContainerType
from log import logging
from utility import Utility
import time
import random
import sys
import re
import threading
import pprint
import yaml

def updateContainerState(containerDic, hostDic):
	try:
		for host in hostDic.values():
			stateList = getContainerStateList(host.getAddress())
			for line in stateList:
				lineSplit = line.split()
				containerDic[lineSplit[0]].setState(lineSplit[1])
		return containerDic
	except Exception as inst:
		print "updateContainerState error"
		print type(inst)
		print inst.args     # arguments stored in .args
		raise

def getContainerStateList(address):
	try:
		lxcCommand = "/usr/bin/lxc-ls -f | awk '{print $1, $2}'"
		res = utility.paramikoWrap(address, lxcCommand)
		return res[2:] 
	except Exception as inst:
		print 'getContainerState error'
		print type(inst)
		print inst.args     # arguments stored in .args
		raise

def generateList(containerDic, hostDic):
	try:
		stopList = []
		runningList = []
		containerDic = updateContainerState(containerDic, hostDic)
		for i in containerDic.values():
			if i.getState() == "RUNNING":
				runningList.append(i)
			elif i.getState() == "STOPPED":
				stopList.append(i)
		return runningList, stopList

	except Exception as inst:
		print "generateList error"
		print type(inst)
		print inst.args     # arguments stored in .args
		raise

def randomTest(minimumTime, MaximumTime, containerDic, hostDic):
	print("Starting chaos...")
	print(time.ctime())

	while 1:
		try:
			runningList, stopList = generateList(containerDic, hostDic)
			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
			for i in runningList:
				print i.getState() + ' \t ' + i.getName()
			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
			for i in stopList:
				print i.getState() + ' \t ' + i.getName()
			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
			ran = random.randint(0, 1)
			t = utility.getRandomInt(MaximumTime-minimumTime)+minimumTime

			if ran == 1:
				if len(stopList) > 10:
					continue
				index = utility.getRandomInt(len(runningList))
				if index != -1:
					name = runningList[index].getName()
					print("About to stop: " + name)
					command = 'lxc-stop -n %s' % name 
					address = hostDic[runningList[index].getPhisicalHost()].getAddress()
					utility.paramikoWrap(address, command)
				else:
					print("Doing nothing for the next %s seconds" % str(t))
			else:
				index = utility.getRandomInt(len(stopList))
				if index != -1:
					name = stopList[index].getName()
					print("About to start: " + name)
					command = 'lxc-start -d -n %s' % name 
					address = hostDic[stopList[index].getPhisicalHost()].getAddress()
					utility.paramikoWrap(address, command)
				else:
					print("Doing nothing for the next %s seconds" % str(t))
			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
			utility.countDown(t)
		except KeyboardInterrupt:
			print("Stoping chaos...")
			sys.exit(0)
		except Exception as inst:
			print type(inst)
			print inst.args
			print(inst)   
			print(time.ctime())
			sys.exit(0)

if __name__ == '__main__':

	##sc = Service()
	##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
	##sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Stop)
	##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
	##sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Start)
	##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
	
	infoParser = InfoParser()
	logger = logging.getLogger('ContainerControl')
	containerDic = infoParser.getAllcontainerDic()
	hostDic = infoParser.getAllhostDic()
	utility = Utility()

	randomTest(20, 40, containerDic, hostDic)
