import yaml
import random
import lxc
from container import Container
from dataContract.containerState import ContainerState
from dataContract.containerType import ContainerType
from cmd.lxcCommandWrap import LXC

containerList = []

def getContainerInfo():
	with open('haha') as data_file:    
		data = yaml.safe_load(data_file)

	for key, value in data['_meta']['hostvars'].iteritems():
		containerList.append(Container(key, value['container_address'], lxc.Container(key).state))


def printContainerInfo(containerName=None):
	for i in containerList:
		if containerName and containerName == i.getName():
			i.setState(lxc.Container(containerName).state)
			print(i.getName() + " : " + i.getAddress() + " : " + i.getState())

def getRandomContainer(container_type):
	if len(container_type) == 0 : return ''
	resultList = []
	for container in containerList:
		name = container.getName()
		if container_type in name:
			resultList.append(name)
	index = random.randrange(0, len(resultList))
	return resultList[index]


l = LXC()
getContainerInfo()
name = getRandomContainer(ContainerType.Rabbit_Mq)
printContainerInfo(name)
l.freeze(name)
printContainerInfo(name)
l.unfreeze(name)
printContainerInfo(name)
l.stop(name)
printContainerInfo(name)
l.start(name)
printContainerInfo(name)
