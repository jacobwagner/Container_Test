from dataContract.infoParser import InfoParser 
from cmd.lxcCommandWrap import LXC
from dataContract.containerState import ContainerState
from dataContract.serviceName import ServiceName
from dataContract.serviceStatus import ServiceStatus
from dataContract.containerType import ContainerType
from log import logging
import time
import random
import paramiko
import sys
import re
import threading
import pprint
import yaml


lxcCommand = "/usr/bin/lxc-ls -f | awk '{print $1, $2}'"

##sc = Service()
##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
##sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Stop)
##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
##sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Start)
##sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)

infoParser = InfoParser()
logger = logging.getLogger('ContainerControl')

containerList = infoParser.getAllContainerList()
hostList = infoParser.getAllHostList()


def updateContainerState(containerList, hostList):
	try:
		containerDic = convertToDic(containerList)
		for host in hostList:
			l = getContainerState(host.getAddress())
			for line in l:
				lineSplit = line.split()
				containerDic[lineSplit[0]].setState(lineSplit[1])
		return containerDic
	except:
		print "updateContainerState error"
		raise

def convertToDic(l):
	try:
		dic = {}
		for i in l:
			dic[i.getName()] = i
		return dic
	except:
		print 'convertToDic error'
		raise
			

def paramikoWrap(address, command):
	try:
		asciiConvertList = []
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(address)
		stdin, stdout, stderr = ssh.exec_command(command)
		for i in stdout.readlines():
			asciiConvertList.append(i.encode('ascii', 'ignore'))
		return asciiConvertList
	except Exception as inst:
		print "generateList error"
		print type(inst)   # the exception instance
		print inst.args     # arguments stored in .args

def getContainerState(address):
	try:
		containerState = []
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(address)
		stdin, stdout, stderr = ssh.exec_command(lxcCommand)
		for i in stdout.readlines()[2:]:
			containerState.append(i.encode('ascii', 'ignore'))
		return containerState
	except:
		print 'getContainerState error'
	finally:
		ssh.close()

def generateList():
	try:
		stopList = []
		runningList = []
		containerDic = updateContainerState(containerList, hostList)
		for i in containerDic.values():
			if i.getState() == "RUNNING":
				runningList.append(i)
			elif i.getState() == "STOPPED":
				stopList.append(i)

		return runningList, stopList

	except Exception as inst:
		print "generateList error"
		print type(inst)   # the exception instance
		print inst.args     # arguments stored in .args
		print("generateList error")
		return [], []
		raise

def randomTest(minimumTime, MaximumTime):
	print("Starting chaos...")
	print(time.ctime())
	l = LXC()

	while 1:
		try:
			runningList, stopList = generateList()
			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
			for i in runningList:
				print i.getState() + ' \t ' + i.getName()
			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
			for i in stopList:
				print i.getState() + ' \t ' + i.getName()
			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
			ran = random.randint(0, 1)
			t = getRandomInt(MaximumTime-minimumTime)+minimumTime
		#	#try get one randome container from running list then stop it
			if ran == 1:
				if len(stopList) > 10:
					continue
				index = getRandomInt(len(runningList))
				if index != -1:
					name = runningList[index].getName()
					print("about to stop: " + name)
					command = 'lxc-stop -n %s' % name 
					hostDic = convertToDic(hostList)
					address = hostDic[runningList[index].getPhisicalHost()].getAddress()
					paramikoWrap(address, command)
				else:
					print("Doing nothing for the next %s seconds" % str(t))
			else:
				index = getRandomInt(len(stopList))
				if index != -1:
					name = stopList[index].getName()
					print("about to start: " + name)
					command = 'lxc-start -d -n %s' % name 
					hostDic = convertToDic(hostList)
					address = hostDic[stopList[index].getPhisicalHost()].getAddress()
					paramikoWrap(address, command)
				else:
					print("Doing nothing for the next %s seconds" % str(t))
			print '----------------------------------------------------------------------------------------------------------------------------------------------------'
			countDown(t)
		except KeyboardInterrupt:
			print("Stoping chaos...")
			sys.exit(0)
		except Exception as inst:
			print type(inst)   # the exception instance
			print inst.args     # arguments stored in .args
			print(type(inst))     # the exception instance
			print(inst.args)      # arguments stored in .args
			print(inst)   
			print(time.ctime())
			sys.exit(0)
			

def getRandomInt(num):
	if num > 0:
		return random.randint(0,num-1)
	else:
		return -1 

def countDown(t):
	if t > 0:
		for i in xrange(t-1, 0, -1):
			print('Sleep for %s seconds' %  str(i))
			sys.stdout.flush()
			time.sleep(1)	

randomTest(20, 40)
