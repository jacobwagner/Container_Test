import yaml
import random
from dataContract.host import Host
from utility import Utility
from dataContract.containerState import ContainerState
from dataContract.containerType import ContainerType
from dataContract.stack import Stack


class InfoParser(object):
    inventory = '/etc/openstack_deploy/openstack_inventory.json'
    stack = Stack.Instance()

    def __init__(self, ):
        with open(self.inventory) as data_file:
            data = yaml.safe_load(data_file)

            if data and data['_meta'] and data['_meta']['hostvars']:
                try:
                    for key, value in data['_meta']['hostvars'].iteritems():
                        self.stack.addHost(key, value['component'], value['container_address'], value['physical_host'])
                except:
                    print("parse inventory error")
                    raise

    def getStackInstance(self):
        return self.stack

    def updateContainerState(self):
        try:
            for host in self.hostDic.values():
                stateList = self.getContainerStateList(host.getAddress())
                for line in stateList:
                    lineSplit = line.split()
                    self.containerDic[lineSplit[0]].setState(lineSplit[1])
        except Exception as inst:
            print "updateContainerState error"
            print type(inst)
            print inst.args  # arguments stored in .args
            raise

    def getContainerStateList(self, address):
        try:
            utility = Utility()
            lxcCommand = "/usr/bin/lxc-ls -f | awk '{print $1, $2}'"
            res = utility.paramikoWrap(address, lxcCommand)
            return res[2:]
        except Exception as inst:
            print 'getContainerState error'
            print type(inst)
            print inst.args  # arguments stored in .args
            raise

    def generateList(self):
        try:
            stopList = []
            runningList = []
            self.updateContainerState()
            for i in self.containerDic.values():
                if i.getState() == "RUNNING":
                    runningList.append(i)
                elif i.getState() == "STOPPED":
                    stopList.append(i)
            return runningList, stopList

        except Exception as inst:
            print "generateList error"
            print type(inst)
            print inst.args  # arguments stored in .args
            raise

    def getHostAddress(self, name):
        try:
            return self.hostDic[name].getAddress()
        except Exception as inst:
            print "getHostAddress error"
            print type(inst)
            print inst.args
