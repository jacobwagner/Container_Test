from dataContract.containerInfo import ContainerInfo
from cmd.lxcCommandWrap import LXC
from dataContract.containerState import ContainerState
from dataContract.serviceName import ServiceName
from dataContract.serviceStatus import ServiceStatus
from dataContract.containerType import ContainerType
import time
import random
import sys


containerInfo = ContainerInfo()
#l = LXC()
#
#def getName():
#	name, ip, status  = containerInfo.getRandomContainer("nova")
#	return name
#
##
##sc = Service()
##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
##sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Stop)
##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
##sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Start)
##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
##
##
##
#
#stoplist = []
#startlist = []
containerList = containerInfo.getAllContainerList()
for i in containerList:
	print i.getName()
#	if i.getState() == "RUNNING":
#		startlist.append(i.getName())
#	elif i.getState() == "STOPPED":
#		stoplist.append(i.getName())
#		l.start(i.getName())
#	
#		
#
#

#while 1:
#	try:
#		name = getName()
#		print "Random Container Name: " + name
#		ran = random.randint(0,2)
#		print "Random number : " + str(ran)
#		if ran == 1:
#			if len(startlist) == 0:
#				pass	
#			else:
#				index = random.randint(0,len(startlist))
#				a = startlist[index]
#				stoplist.append(a)
#				startlist.remove(a)
#				l.stop(a)
#				print "stop : " + a
#		else:
#			if len(stoplist) == 0:
#				pass
#			else:
#				index = random.randint(0,len(stoplist))
#				a = stoplist[index]
#				stoplist.remove(a)
#				startlist.append(a)	
#				l.start(a)
#				print "start : " + a
#	except KeyboardInterrupt:
#		sys.exit(0)
#	except:
#		continue
#	time.sleep(30)
	
#containerInfo.printContainerInfo(name)
#l.freeze(name)
#containerInfo.printContainerInfo(name)
#print("after")
#
#
#l.unfreeze(name)
#containerInfo.printContainerInfo(name)
#l.stop(name)
#containerInfo.printContainerInfo(name)
#l.start(name)
#containerInfo.printContainerInfo(name)
