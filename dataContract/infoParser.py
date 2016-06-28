import yaml
import random
from dataContract.container import Container
from dataContract.host import Host
from dataContract.containerState import ContainerState
from dataContract.containerType import ContainerType

class InfoParser:
	containerDic = {}
	hostDic = {}
	inventory = '/etc/openstack_deploy/openstack_inventory.json'

	def __init__(self):
		with open(self.inventory) as data_file:    
			data = yaml.safe_load(data_file)
	
			if data and data['_meta'] and data['_meta']['hostvars']:
				try:
 					for key, value in data['_meta']['hostvars'].iteritems():
						if value['component']:
							self.containerDic[key] = Container(key, value['component'], value['container_address'], value['physical_host'])
						elif not value['component'] and value['physical_host'] == key:
							self.hostDic[key] = Host(key, value['container_address'])
						else:
							print("parse inventory error")
							raise
				except:
					print("parse inventory error")
					raise
	
	def printInfo(self, containerName=None):
		if not containerName:
			print 'Container List : '
			for i in self.containerDic.values():
				print(i.getName() + " : " + i.getAddress() + " : "  + i.getType() + " : " + i.getPhisicalHost())
			print 'Host List'
			for i in self.hostDic.values():
				print(i.hostGetName() + " : " + i.hostGetAddress())
		else:
			for i in self.containerDic.values():
				if containerName == i.getName():
					print(i.getName() + " : " + i.getAddress() + " : " + i.getState())

	def getAllcontainerDic(self):
		return self.containerDic
		
	def getAllhostDic(self):
		return self.hostDic

