from log import logging

logger = logging.getLogger()

class Host(object):

    def __init__(self, name, host=None, address=None, component=None, ssh_key=None, state='UNKNOWN'):
        self.__name = name
        self.__host = host
        self.__address = address
        self.__component = component
        self.__hostDic = {}
        self.__ssh_key = ssh_key
        self.__state = state

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getHost(self):
        return self.__host

    def setHost(self, host):
        self.__host = host

    def getAddress(self):
        return self.__address

    def setAddress(self, address):
        self.__address = address

    def getComponent(self):
        return self.__component

    def setComponent(self, component):
        self.__component = component

    def setSshKey(self, ssh_key):
        self.__ssh_key = ssh_key

    def getSSHKey(self):
        return self.__ssh_key

    def getState(self):
        return self.__state

    def setState(self, state):
        self.__state = state

    def getHostDic(self):
        return self.__hostDic

    def addToHostDic(self, host):
        try:
            if host.getName() in self.__hostDic:
                logger.error(str(inspect.stack()[0][3]) + ' host exist')
                raise
            else:
                self.__hostDic[host.getName()] = host
        except:
            logger.error(str(inspect.stack()[0][3]))
            logger.info('calling func : '+str(inspect.stack()[1][3]) + '() from ' + str(inspect.stack()[1][1]))
            raise

    def getHostDic(self):
        return self.__hostDic
