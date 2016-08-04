class Host(object):
    __name = ''
    __host = ''
    __address = ''
    __component = ''
    __hostDic = {}
    __ssh_key = ''
    __state = ''

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
                print 'addNodeToDic error'
                raise
            else:
                self.__hostDic[host.getName()] = host
        except:
            print 'addNodeToDic error'
            raise

    def getHostDic(self):
        return self.__hostDic
