class Host:

	def __init__(self, name, address=None, component=None, ssh_key=None):
		self.name = name
		self.address = address
		self.nodeDic = {}
		self.ssh_key = ssh_key 
		self.component = component

	def getName(self):
		return self.name

	def getAddress(self):
		return self.address

	def setAddress(self, address):
		self.address = address

	def setComponent(self, component):
		self.component = component 

	def setSshKey(self, ssh_key):
		self.ssh_key = ssh_key 

	def getSSHKey(self):
		return self.ssh_key

	def addNodeToDic(self, node):
		try:
			if node.getName() in self.nodeDic:
				print 'addNodeToDic error'
				raise
			else:
				self.nodeDic[node.getName()] = node
		except:
			print 'addNodeToDic error'
			raise
	def getNodeDic(self):
		return self.nodeDic
			
			
