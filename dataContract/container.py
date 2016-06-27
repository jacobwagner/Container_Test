from dataContract.containerState import ContainerState

class Container:
	container_name = ''
	container_type = ''
	container_address = ''
	container_state = ''
	container_physical_host = ''

	def __init__(self, name, ctype, address, physical_host, state=ContainerState.UNKNOWN):
		self.container_name = name
		self.container_type = ctype
		self.container_address = address
		self.container_state = state
		self.container_physical_host = physical_host

	def getName(self):
		return self.container_name

	def getAddress(self):
		return self.container_address

	def getState(self):
		return self.container_state

	def getType(self):
		return self.container_type

	def getPhisicalHost(self):
		return self.container_physical_host

	def setState(self, state):
		self.container_state = state
