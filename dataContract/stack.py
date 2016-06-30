from dataContract.node import Node 
from dataContract.host import Host
from dataContract.singleton import Singleton 
import random
import paramiko

@Singleton
class Stack(object):
	

	def __init__(self):
		self.hosts = {}

	def addHost(self, name, component = None, address = None, ssh_key = None):
		try:
			if not name:
				print 'addHost empty name'
				raise
			if name not in self.hosts:
				self.hosts[name] = Host(name, address, component, ssh_key)
			else:
				self.hosts[name].setAddress(address)
				self.hosts[name].setComponent(component)
				self.hosts[name].setSshKey(ssh_key)
		except Exception as inst:
			print 'addHost error'
			print type(inst)
			print inst.args
			raise
				
	def addNode(self, name, component, address, host, state=None):
		try:
			if not host or not name or not component or not address:
				print 'empty info'
				raise
			if host not in self.hosts:
				self.addHost(host)
			self.hosts[host].addNodeToDic(Node(name, component, address, host))
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
			print host.getName(), '\t', host.getAddress(), '\t', host.getComponent()
			for node in host.getNodeDic().values():
				print '\t|-------' + node.getName(), '\t', node.getAddress(), '\t', node.getComponent(), '\t', node.getState()

	def getRandomHost(self):
		try:
			hostList = []
			for host in self.hosts.values():
				if host.getComponent():
						hostList.append(host)
			index = self.getRandomInt(len(hostList))
			return hostList[index]
		except Exception as inst:
			print 'getRandomHost error'
			print type(inst)
			print inst.args
			raise
	
	def getRandomNode(self):
		try:
			nodeList = []
			for host in self.hosts.values():
				if not host.getComponent():
					for node in host.getNodeDic().values():
						nodeList.append(node)
			index = self.getRandomInt(len(nodeList))
			return nodeList[index]
		except Exception as inst:
			print 'getRandomNode error'
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
						self.hosts[host.getName()].nodeDic[lineSplit[0]].setState(lineSplit[1])
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
			self.updateContainerState()
			for i in self.containerDic.values():
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
			print "paramikoWrap error"
			print type(inst)
			print inst.args

		
