import yaml
import random
import paramiko
from dataContract.container import Container
from dataContract.host import Host
from dataContract.containerState import ContainerState
from dataContract.containerType import ContainerType

class InfoParser:
	containerList = []
	hostList = []
	inventory = '/etc/openstack_deploy/openstack_inventory.json'

	def __init__(self):
		with open(self.inventory) as data_file:    
			data = yaml.safe_load(data_file)
	
			if data and data['_meta'] and data['_meta']['hostvars']:
				try:
 					for key, value in data['_meta']['hostvars'].iteritems():
						if value['component']:
							self.containerList.append(Container(key, value['component'], value['container_address'], value['physical_host']))
						elif not value['component'] and value['physical_host'] == key:
							self.hostList.append(Host(key, value['container_address']))
						else:
							print("parse inventory error")
							raise
				except:
					print("parse inventory error")
					raise
	
	def printInfo(self, containerName=None):
		if not containerName:
			print 'Container List : '
			for i in self.containerList:
				print(i.getName() + " : " + i.getAddress() + " : "  + i.getType() + " : " + i.getPhisicalHost())
			print 'Host List'
			for i in self.hostList:
				print(i.hostGetName() + " : " + i.hostGetAddress())
		else:
			for i in self.containerList:
				if containerName == i.getName():
					print(i.getName() + " : " + i.getAddress() + " : " + i.getState())
	
	def getRandomContainer(self, container_type):
		if len(container_type) == 0 : return ''
		resultList = []
		for container in self.containerList:
			name = container.getName()
			if container_type in name:
				resultList.append([name, container.getAddress(), container.getState()])
		index = random.randrange(0, len(resultList))
		return resultList[index]

	def getAllContainerList(self):
		return self.containerList
		
	def getAllHostList(self):
		return self.hostList

