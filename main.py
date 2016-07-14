from dataContract.infoParser import InfoParser
from cmd.lxcCommandWrap import LXC
from dataContract.containerState import ContainerState
from dataContract.serviceName import ServiceName
from dataContract.serviceStatus import ServiceStatus
from dataContract.containerType import ContainerType
from dataContract.stack import Stack
from log import logging
from utility import Utility
import time
import random
import sys
import re
import threading
import pprint
import os
import yaml

# def containerControl(minimumTime, MaximumTime):
#	print("Starting chaos...")
#	print(time.ctime())
#	infoParser = InfoParser()
#	utility = Utility()
#
#	while 1:
#		try:
#			runningList, stopList = infoParser.generateList()
#			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
#			for i in runningList:
#				print i.getState() + ' \t ' + i.getName()
#			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
#			for i in stopList:
#				print i.getState() + ' \t ' + i.getName()
#			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
#			ran = random.randint(0, 1)
#			t = utility.getRandomInt(MaximumTime-minimumTime)+minimumTime
#
#			if ran == 1:
#				if len(stopList) > 10:
#					continue
#				index = utility.getRandomInt(len(runningList))
#				if index != -1:
#					name = runningList[index].getName()
#					print("About to stop: " + name)
#					command = 'lxc-stop -n %s' % name 
#					address = infoParser.getHostAddress(runningList[index].getPhisicalHost())
#					utility.paramikoWrap(address, command)
#				else:
#					print("Doing nothing for the next %s seconds" % str(t))
#			else:
#				index = utility.getRandomInt(len(stopList))
#				if index != -1:
#					name = stopList[index].getName()
#					print("About to start: " + name)
#					command = 'lxc-start -d -n %s' % name 
#					address = infoParser.getHostAddress(stopList[index].getPhisicalHost())
#					utility.paramikoWrap(address, command)
#				else:
#					print("Doing nothing for the next %s seconds" % str(t))
#			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
#			utility.countDown(t)
#		except KeyboardInterrupt:
#			print("Stoping chaos...")
#			sys.exit(0)
#		except Exception as inst:
#			print type(inst)
#			print inst.args
#			print(inst)   
#			print(time.ctime())
#			sys.exit(0)
#
if __name__ == '__main__':
    ##sc = Service()
    ##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
    ##sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Stop)
    ##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
    ##sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Start)
    ##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)

    logger = logging.getLogger('ContainerControl')

    infoParser = InfoParser()
    stack = infoParser.getStackInstance()
   # stack.updateServicesState()


# stack.updateHostState()
    stack.createChaos()

#	node = stack.getRandomNode()
#	print node.getName(), node.getAddress(), node.getComponent()
#	host = stack.getRandomHost()
#	print host.getName(), host.getAddress(), host.getComponent()
