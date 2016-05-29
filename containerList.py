import yaml
import random
import lxc
from container import Container
from containerState import ContainerState
from containerType import ContainerType

containerList = []

def getContainerInfo():
	with open('haha') as data_file:    
		data = yaml.safe_load(data_file)

	for key, value in data['_meta']['hostvars'].iteritems():
		containerList.append(Container(key, value['container_address'], lxc.Container(key).state))


def printContainerInfo():
	for i in containerList:
		print(i.getName() + " : " + i.getAddress() + " : " + i.getState())

def getRandomContainer(container_type):
	if len(container_type) == 0 : return ''
	resultList = []
	for container in containerList:
		name = container.getName()
		if container_type in name:
			resultList.append(name)
	index = random.randrange(0, len(resultList))
	print(index)
	return resultList[index]












getContainerInfo()
print(getRandomContainer(ContainerType.Rabbit_Mq))
print(getRandomContainer(ContainerType.Rabbit_Mq))
print(getRandomContainer(ContainerType.Rabbit_Mq))
