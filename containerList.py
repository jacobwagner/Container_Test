import yaml
import lxc
from container import Container
from containerState import ContainerState

containerList = []

def getContainerInfo():
	with open('haha') as data_file:    
		data = yaml.safe_load(data_file)

	for key, value in data['_meta']['hostvars'].iteritems():
		containerList.append(Container(key, value['container_address'], lxc.Container(key).state))


def printContainerInfo():
	for i in containerList:
		print(i.getName() + " : " + i.getAddress() + " : " + i.getState())

getContainerInfo()
printContainerInfo()
