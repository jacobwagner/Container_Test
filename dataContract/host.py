class Host:
	host_name = ''
	host_address = ''

	def __init__(self, name, address):
		self.host_name = name
		self.host_address = address


	def getName(self):
		return self.host_name

	def getAddress(self):
		return self.host_address
