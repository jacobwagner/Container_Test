from containerState import ContainerState

class Container:
	container_name = ''
	container_address = ''
	container_state = ''
	

	def __init__(self, name, address, state=ContainerState.UNKNOWN):
		self.container_name = name
		self.container_address = address
		self.container_state = state

	def getName(self):
		return self.container_name

	def getAddress(self):
		return self.container_address

	def getState(self):
		return self.container_state


