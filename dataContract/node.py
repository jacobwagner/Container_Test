from dataContract.containerState import ContainerState

class Node:

	def __init__(self, name, component, address, host, state=ContainerState.UNKNOWN):
		self.name = name
		self.component  = component 
		self.address = address
		self.state = state
		self.host = host

	def getName(self):
		return self.name

	def getAddress(self):
		return self.address

	def getComponent(self):
		return self.component

	def getState(self):
		return self.state

	def getType(self):
		return self.type

	def getHost(self):
		return self.host

	def setState(self, state):
		self.state = state
