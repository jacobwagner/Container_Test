from dataContract.containerInfo import ContainerInfo
from cmd.lxcCommandWrap import LXC
from cmd.serviceCommandWrap import Service
from dataContract.containerState import ContainerState
from dataContract.serviceName import ServiceName
from dataContract.serviceStatus import ServiceStatus
from dataContract.containerType import ContainerType


containerInfo = ContainerInfo()
l = LXC()

name, ip, status  = containerInfo.getRandomContainer(ContainerType.Memcached)
#
sc = Service()
sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Stop)
sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)
sc.runServiceCommand(ip, ServiceName.Memcached, ServiceStatus.Start)
sc.checkServiceStatus(ip, ServiceName.Memcached, ServiceStatus.Status)

#
#
#print("before")
#containerInfo.printContainerInfo(name)
#l.freeze(name)
#containerInfo.printContainerInfo(name)
#print("after")
#
#
#l.unfreeze(name)
#containerInfo.printContainerInfo(name)
#l.stop(name)
#containerInfo.printContainerInfo(name)
#l.start(name)
#containerInfo.printContainerInfo(name)
