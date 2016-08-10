import yaml
import random
from dataContract.host import Host
from utility import Utility
from dataContract.containerState import ContainerState
from dataContract.containerType import ContainerType
from dataContract.stack import Stack
from log import logging
import inspect


logger = logging.getLogger('chaos.infoparser')


class InfoParser(object):

    #parse the inventory file and generate a stack instance 
    inventory = '/etc/openstack_deploy/openstack_inventory.json'
    logger.info(inventory)
    stack = Stack.Instance()

    def __init__(self):
        with open(self.inventory) as data_file:
            data = yaml.safe_load(data_file)

            if data and data['_meta'] and data['_meta']['hostvars']:
                try:
                    for key, value in data['_meta']['hostvars'].iteritems():
                        self.stack.addHost(key, value['component'], value['container_address'], value['physical_host'])
                except:
                    logger.error(str(inspect.stack()[0][3]))
                    logger.info('calling func : '+str(inspect.stack()[1][3]) + '() from ' + str(inspect.stack()[1][1]))
                    raise

    def getStackInstance(self):
        return self.stack
