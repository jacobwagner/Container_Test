from dataContract.containerInfo import ContainerInfo
from cmd.lxcCommandWrap import LXC
from cmd.serviceCheck import ServiceCheck
from dataContract.containerState import ContainerState
from dataContract.serviceName import ServiceName
from dataContract.serviceStatus import ServiceStatus
from dataContract.containerType import ContainerType


containerInfo = ContainerInfo()
l = LXC()

name, ip, status  = containerInfo.getRandomContainer(ContainerType.Rabbit_Mq)
#
#sc = ServiceCheck()
#sc.checkServiceStatus(ip, ServiceName.RabbitMQ_Server, ServiceStatus.Status)


print("before")
containerInfo.printContainerInfo(name)
l.freeze(name)
containerInfo.printContainerInfo(name)
print("after")


l.unfreeze(name)
containerInfo.printContainerInfo(name)
l.stop(name)
containerInfo.printContainerInfo(name)
l.start(name)
containerInfo.printContainerInfo(name)
