from dataContract.node import Node 
from dataContract.host import Host
from dataContract.singleton import Singleton 

@Singleton
class Stack:
	

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

	@staticmethod
	def getRandomInt(num):
		if num > 0:
			return random.randint(0,num-1)
		else:
			return -1

	def printStack(self):
		for host in self.hosts.values():
			print host.getName()
			for node in host.getNodeDic().values():
				print '\t|-------' + node.getName()
