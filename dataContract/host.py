class Host(object):

	def __init__(self, name, host=None, address=None, component=None, ssh_key=None, state='UNKNOWN'):
		self.name = name
		self.host = host
		self.address = address
		self.component = component
		self.hostDic = {}
		self.ssh_key = ssh_key 
		self.state = state

	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name

	def getHost(self):
		return self.host

	def setHost(self, host):
		self.host = host

	def getAddress(self):
		return self.address

	def setAddress(self, address):
		self.address = address

	def getComponent(self):
		return self.component

	def setComponent(self, component):
		self.component = component 

	def setSshKey(self, ssh_key):
		self.ssh_key = ssh_key 

	def getSSHKey(self):
		return self.ssh_key

	def getState(self):
		return self.state

	def setState(self, state):
		self.state = state

	def addToHostDic(self, host):
		try:
			if host.getName() in self.hostDic:
				print 'addNodeToDic error'
				raise
			else:
				self.hostDic[host.getName()] = host 
		except:
			print 'addNodeToDic error'
			raise

	def getHostDic(self):
		return self.hostDic
			
			
