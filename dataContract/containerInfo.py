import yaml
import random
import paramiko
import lxc
from dataContract.container import Container
from dataContract.containerState import ContainerState
from dataContract.containerType import ContainerType

class ContainerInfo:
	containerList = []
	inventory = '/etc/openstack_deploy/openstack_inventory.json'
	prefix = ''

	def __init__(self):
		with open(self.inventory) as data_file:    
			data = yaml.safe_load(data_file)
	
			if data and data['_meta'] and data['_meta']['hostvars']:
				try:
					for key, value in data['_meta']['hostvars'].iteritems():
						if value['container_address'] != "172.29.236.100":
							self.containerList.append(Container(key, value['container_address'], lxc.Container(key).state))
						else:
							self.prefix = key
				except:
					print("parse inventory error")
					raise
	
	def printContainerInfo(self, containerName=None):
		if not containerName:
			for i in self.containerList:
				print(i.getName() + " : " + i.getAddress() + " : " + i.getState())
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
		
	def getContainerPrefix(self):
		return self.prefix

