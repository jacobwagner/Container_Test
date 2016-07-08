from dataContract.host import Host
from dataContract.singleton import Singleton 
from dataContract.servicesParser import ServicesParser 
from multiprocessing import pool
import random
import paramiko
import time
import os
import sys

@Singleton
class Stack(object):

	def __init__(self):
		self.hosts = {}

	def addHost(self, name, component, address, host, ssh_key = None):
		try:
			if not name:
				print 'addHost empty name'
				raise
			#host with multiple containers with no component
			if not component and name == host:
				if name not in self.hosts:
					self.hosts[name] = Host(name, host, address, component, ssh_key)
				else:
					self.hosts[name].setAddress(address)
					self.hosts[name].setComponent(component)
					self.hosts[name].setSshKey(ssh_key)
			#host has component
			elif component and name == host:
				if name not in self.hosts:
					self.hosts[name] = Host(name, host, address, component, ssh_key)
				else:
					self.hosts[name].setAddress(address)
					self.hosts[name].setComponent(component)
					self.hosts[name].setSshKey(ssh_key)
			elif component and name != host:
				if host in self.hosts:
					self.hosts[host].addToHostDic(Host(name, host, address, component, ssh_key))
				else:
					self.hosts[host] = Host(host)
					self.hosts[host].addToHostDic(Host(name, host, address, component, ssh_key))
			else:
				print "addHost error"
				raise
		except Exception as inst:
			print 'addHost error'
			print type(inst)
			print inst.args
			raise

	def getRandomInt(self, num):
		if num > 0:
			return random.randint(0,num-1)
		else:
			return -1

	def printStack(self):
		for host in self.hosts.values():
			print (str(host.getAddress()) + '\t' + str(host.getComponent()) + '\t' + str(host.getName())).format()
			for node in host.getHostDic().values():
				print ('\t|-------' + str(node.getState()) + '\t' + str(node.getAddress()) + '\t' + str(node.getName()) + '\t' + str(node.getComponent())).format()

	#get all the host which has component.
	def getHostList(self):
		try:
			hostList = []
			for host in self.hosts.values():
				if not host.getComponent():
					if len(host.getHostDic()) != 0:
						for i in host.getHostDic().values():
							hostList.append(i)
				else:
					hostList.append(host)
			return hostList
		except Exception as inst:
			print 'getServiceDic error'
			print type(inst)
			print inst.args
			raise
		
	#Go to each host and check the service running/stop
	def updateServicesState(self):
		try:
			
			
			hostList = self.getHostList()
			dic = ServicesParser.getServiceDic()
			for host in hostList:
				print host.getName(), host.getComponent(), host.getAddress()
				for service in dic[host.getComponent()]:
					if 'running'in str(self.paramikoWrap(host.getAddress(), 'service ' + service + ' status')):
						print '\t\t\t|--------------', service, '  running' 
					else:
						print '\t\t\t|--------------', service, '  not running' 
		except Exception as inst:
			print inst.args
			print '\t\t\t|--------------', service, '  not running' 
		

	def getRandomHost(self):
		try:
			hostList = self.getHostList()
			index = self.getRandomInt(len(hostList))
			return hostList[index]
		except Exception as inst:
			print 'getRandomHost error'
			print type(inst)
			print inst.args
			raise

	def updateNodeState(self):
		try:
			for host in self.hosts.values():
				if not host.getComponent():
					stateList = self.getContainerStateList(host.getAddress())
					for line in stateList:
						lineSplit = line.split()
						self.hosts[host.getName()].getHostDic()[lineSplit[0]].setState(lineSplit[1])
		except Exception as inst:
			print "updateContainerState error"
			print type(inst)
			print inst.args     # arguments stored in .args
			raise
	
	def getContainerStateList(self, address):
		try:
			lxcCommand = "/usr/bin/lxc-ls -f | awk '{print $1, $2}'"
			res = self.paramikoWrap(address, lxcCommand)
			return res[2:] 
		except Exception as inst:
			print 'getContainerState error'
			print type(inst)
			print inst.args     # arguments stored in .args
			raise

	def generateList(self):
		try:
			stopList = []
			runningList = []
			self.updateNodeState()
			for host in self.hosts.values():
				if not host.getComponent():
					for node in host.getHostDic().values():
						if node.getState() == "RUNNING":
							runningList.append(node)
						elif node.getState() == "STOPPED":
							stopList.append(node)
			return runningList, stopList
		except Exception as inst:
			print "generateList error"
			print type(inst)
			print inst.args     # arguments stored in .args
			raise

	def paramikoWrap(self, address, command):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(address)
			stdin, stdout, stderr = ssh.exec_command(command)
			resList = []
			for line in stdout.readlines():
				resList.append(line.encode('ascii', 'ignore'))
			return resList 
		except Exception as inst:
			pass

	def createChaos(self, typ='container', maximumTime=30, minimumTime=20):
			if typ == 'container':
				self.containerChaos(maximumTime, minimumTime)

	def getHostAddress(self, hostname):
		try:
			if hostname:
				return self.hosts[hostname].getAddress()
		except Exception as inst:
			print "getHostAddress error"
			print type(inst)
			print inst.args
	
			
	def containerChaos(self, maximumTime, minimumTime):
		try:
			while 1:
				runningList, stopList = self.generateList()
				print '----------------------------------------------------------------------------------------------------------------------------------------------------'
				for i in runningList:
					print i.getState() + ' \t ' + i.getName()
				print '----------------------------------------------------------------------------------------------------------------------------------------------------'
				for i in stopList:
					print i.getState() + ' \t ' + i.getName()
				print '----------------------------------------------------------------------------------------------------------------------------------------------------'
				ran = random.randint(0, 1)
				t = self.getRandomInt(maximumTime-minimumTime)+minimumTime
				if ran == 1:
					if len(stopList) > 10:
						continue
					index = self.getRandomInt(len(runningList))
					if index != -1:
						name = runningList[index].getName()
						print("About to stop: " + name)
						command = 'lxc-stop -n %s' % name
						address = self.getHostAddress(runningList[index].getHost())
						#self.paramikoWrap(address, command)
					else:
						print("Doing nothing for the next %s seconds" % str(t))
				else:
					index = self.getRandomInt(len(stopList))
					if index != -1:
						name = stopList[index].getName()
						print("About to start: " + name)
						command = 'lxc-start -d -n %s' % name
						address = self.getHostAddress(stopList[index].getHost())
						#self.paramikoWrap(address, command)
					else:
						print("Doing nothing for the next %s seconds" % str(t))
					print '----------------------------------------------------------------------------------------------------------------------------------------------------'
				self.countDown(t)
		except KeyboardInterrupt:
			print("Stoping chaos...")
			sys.exit(0)
		except Exception as inst:
			print type(inst)
			print inst.args
			print(inst)
			print(time.ctime())
			sys.exit(0)



	def countDown(self, t):
		if t > 0:
			for i in xrange(t-1, 0, -1):
				print('Sleep for %s seconds' %  str(i))
				sys.stdout.flush()
				time.sleep(1)


















		
