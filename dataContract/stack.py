from dataContract.host import Host
from dataContract.singleton import Singleton
from multiprocessing import Pool
from dataContract.servicesParser import ServicesParser
from multiprocessing import pool
import random
import paramiko
import time
import os
import sys



@Singleton
class Stack(object):
    def __init__(self):
        self.hosts = {}

    def addHost(self, name, component, address, host, ssh_key=None):
        try:
            if not name:
                print 'addHost empty name'
                raise
            # host with multiple containers with no component
            if not component and name == host:
                if name not in self.hosts:
                    self.hosts[name] = Host(name, host, address, component, ssh_key)
                else:
                    self.hosts[name].setAddress(address)
                    self.hosts[name].setComponent(component)
                    self.hosts[name].setSshKey(ssh_key)
            # host has component
            elif component and name == host:
                if name not in self.hosts:
                    self.hosts[name] = Host(name, host, address, component, ssh_key)
                else:
                    self.hosts[name].setAddress(address)
                    self.hosts[name].setComponent(component)
                    self.hosts[name].setSshKey(ssh_key)
            elif component and name != host:
                if host in self.hosts:
                    self.hosts[host].addToHostDic(Host(name, host, address, component, ssh_key))
                else:
                    self.hosts[host] = Host(host)
                    self.hosts[host].addToHostDic(Host(name, host, address, component, ssh_key))
            else:
                print "addHost error"
                raise
        except Exception as inst:
            print 'addHost error'
            print type(inst)
            print inst.args
            raise

    def getRandomInt(self, num):
        if num > 0:
            return random.randint(0, num - 1)
        else:
            return -1

    def printStack(self):
        for host in self.hosts.values():
            print (str(host.getAddress()) + '\t' + str(host.getComponent()) + '\t' + str(host.getName())).format()
            for node in host.getHostDic().values():
                print ('\t|-------' + str(node.getState()) + '\t' + str(node.getAddress()) + '\t' + str(
                    node.getName()) + '\t' + str(node.getComponent())).format()

    # get all the host which has component.
    def getHostList(self):
        try:
            hostList = []
            for host in self.hosts.values():
                if not host.getComponent():
                    if len(host.getHostDic()) != 0:
                        for i in host.getHostDic().values():
                            hostList.append(i)
                else:
                    hostList.append(host)
            return hostList
        except Exception as inst:
            print 'getServiceDic error'
            print type(inst)
            print inst.args
            raise

    def updateServicesState(self):
        try:
            hostList = self.getHostList()
            dic = ServicesParser.getServiceDic()
            pool = Pool(processes=10)
            jobList = []
            for host in hostList:
                for service in dic[host.getComponent()]:
                    if service != "":
                        jobList.append([host.getAddress(), service, ' status', 'unknown', host.getComponent()])
            it = pool.imap(doJob, jobList)
            serviceStateDic = {}
            for item in it:
                if item[4] not in serviceStateDic:
                    serviceStateDic[item[4]] = { item[0] : item[3] }
                else:
                    if item[0] in serviceStateDic[item[4]]:
                        if item[3] == 'stop':
                            serviceStateDic[item[4]][item[0]] = 'stop'
                        elif item[3] == 'unknown':
                            serviceStateDic[item[4]][item[0]] = 'unknown'
                    else:
                        serviceStateDic[item[4]][item[0]] = item[3]
            return serviceStateDic

        except KeyboardInterrupt:
            print("Stopping chaos...")
            sys.exit(0)
        except Exception as inst:
            print "updateServiceState exception"
            print inst.args

    def getRandomHost(self):
        try:
            hostList = self.getHostList()
            index = self.getRandomInt(len(hostList))
            return hostList[index]
        except Exception as inst:
            print 'getRandomHost error'
            print type(inst)
            print inst.args
            raise

    def updateHostState(self):
        try:
            for host in self.hosts.values():
                if not host.getComponent():
                    stateList = self.getContainerStateList(host.getAddress())
                    for line in stateList:
                        lineSplit = line.split()
                        self.hosts[host.getName()].getHostDic()[lineSplit[0]].setState(lineSplit[1])
        except Exception as inst:
            print "updateContainerState error"
            print type(inst)
            print inst.args  # arguments stored in .args
            raise

    def getContainerStateList(self, address):
        try:
            lxcCommand = "/usr/bin/lxc-ls -f | awk '{print $1, $2}'"
            res = self.paramikoWrap(address, lxcCommand)
            return res[2:]
        except Exception as inst:
            print 'getContainerState error'
            print type(inst)
            print inst.args  # arguments stored in .args
            raise

    def generateHostList(self):
        try:
            stopList = []
            runningList = []
            self.updateHostState()
            for host in self.hosts.values():
                if not host.getComponent():
                    for node in host.getHostDic().values():
                        if node.getState() == "RUNNING":
                            runningList.append(node)
                        elif node.getState() == "STOPPED":
                            stopList.append(node)
            return runningList, stopList
        except Exception as inst:
            print "generateHostList error"
            print type(inst)
            print inst.args  # arguments stored in .args
            raise

    def paramikoWrap(self, address, command):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(address)
            stdin, stdout, stderr = ssh.exec_command(command)
            resList = []
            for line in stdout.readlines():
                resList.append(line.encode('ascii', 'ignore'))
            return resList
        except Exception as inst:
            pass

    def createChaos(self, typ='service', maximumTime=30, minimumTime=20):
        try:
            if typ == 'container':
                self.containerChaos(maximumTime, minimumTime)
            elif typ == 'service':
                self.serviceChaos(maximumTime, minimumTime)
        except KeyboardInterrupt:
            print("Stopping chaos...")
            sys.exit(0)

    def getHostAddress(self, hostname):
        try:
            if hostname:
                return self.hosts[hostname].getAddress()
        except Exception as inst:
            print "getHostAddress error"
            print type(inst)
            print inst.args

    def serviceChaos(self, maximumTime, minimumTime):
        try:
            dic = ServicesParser.getServiceDic()
            pool = Pool(processes=2)
            while 1:
                t = self.getRandomInt(maximumTime - minimumTime) + minimumTime
                self.countDown(t)
                serviceDic = self.updateServicesState()
                componentList = serviceDic.keys()

                runningList, stopList = self.generateServiceList(serviceDic)
                ran = random.randint(0, 1)
                address = ''
                randomComponent = ''
                jobList = []
                cmd = ''
                if ran:
                    index = self.getRandomInt(len(runningList))
                    if index != -1:
                        print "1"
                        cmd = 'stop'
                        randomComponent = runningList[index]
                        addressList = serviceDic[randomComponent].keys()
                        address = addressList[self.getRandomInt(len(addressList))]
                        print address, randomComponent
                    else:
                        print "2"
                        print "Doing nothing"
                        continue
                else:
                    index = self.getRandomInt(len(stopList))
                    if index != -1:
                        print "3"
                        cmd = 'start'
                        randomComponent = stopList[index]
                        addressList = serviceDic[randomComponent].keys()
                        address = addressList[self.getRandomInt(len(addressList))]
                        print address, randomComponent
                    else:
                        print "4"
                        print "Doing nothing"
                        continue

                for service in dic[randomComponent]:
                    if service != "":
                        jobList.append([address, service, cmd, 'unknown', randomComponent])
                print jobList
                #it = pool.imap(doJob, jobList)
  
        except KeyboardInterrupt:
            print("Stopping chaos...")
            sys.exit(0)
        except Exception as inst:
            print "serviceChaos error"
            print type(inst)
            print inst.args
            print(inst)
            sys.exit(0)

    def generateServiceList(self, serviceDic):
        try:
            runningList = []
            stopList = []
            for key in serviceDic.keys():
                state = self.checkListState(serviceDic[key].values())
                if state == 'running':
                    runningList.append(key)
                elif state == 'stop':
                    stopList.append(key)
            return runningList, stopList

        except Exception as inst:
            print "serviceChaos error"
            print type(inst)
            print inst.args
            print(inst)
            sys.exit(0)

    def checkListState(self, stateList):
        try:
            state = 'running'
            for i in stateList:
                if i == 'stop':
                    state = 'stop'
                elif i == 'unknown':
                    state = 'unknown'
                    return state
            return state

        except Exception as inst:
            print "checkListState error"
            print type(inst)
            print inst.args
            print(inst)
            sys.exit(0)

    def containerChaos(self, maximumTime, minimumTime):
        try:
            while 1:
                runningList, stopList = self.generateHostList()
                print '----------------------------------------------------------------------------------------------------------------------------------------------------'
                for i in runningList:
                    print i.getState() + ' \t ' + i.getName()
                print '----------------------------------------------------------------------------------------------------------------------------------------------------'
                for i in stopList:
                    print i.getState() + ' \t ' + i.getName()
                print '----------------------------------------------------------------------------------------------------------------------------------------------------'
                ran = random.randint(0, 1)
                t = self.getRandomInt(maximumTime - minimumTime) + minimumTime
                if ran == 1:
                    if len(stopList) > 10:
                        continue
                    index = self.getRandomInt(len(runningList))
                    if index != -1:
                        name = runningList[index].getName()
                        print("About to stop: " + name)
                        command = 'lxc-stop -n %s' % name
                        address = self.getHostAddress(runningList[index].getHost())
                    # self.paramikoWrap(address, command)
                    else:
                        print("Doing nothing for the next %s seconds" % str(t))
                else:
                    index = self.getRandomInt(len(stopList))
                    if index != -1:
                        name = stopList[index].getName()
                        print("About to start: " + name)
                        command = 'lxc-start -d -n %s' % name
                        address = self.getHostAddress(stopList[index].getHost())
                    # self.paramikoWrap(address, command)
                    else:
                        print("Doing nothing for the next %s seconds" % str(t))
                    print '----------------------------------------------------------------------------------------------------------------------------------------------------'
                self.countDown(t)
        except KeyboardInterrupt:
            print("Stoping chaos...")
            sys.exit(0)
        except Exception as inst:
            print type(inst)
            print inst.args
            print(inst)
            print(time.ctime())
            sys.exit(0)

    def countDown(self, t):
        if t > 0:
            for i in xrange(t - 1, 0, -1):
                print('Sleep for %s seconds' % str(i))
                sys.stdout.flush()
                time.sleep(1)


def doJob(jobList):
    try:
        if jobList[1]:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(jobList[0])
            stdin, stdout, stderr = ssh.exec_command('service ' + jobList[1] + jobList[2])
            resList = []
            for line in stdout.readlines():
                resList.append(line.encode('ascii', 'ignore'))
            if 'running' in str(resList):
                jobList[3] = 'running'
            elif 'stop' in str(resList):
                jobList[3] = 'stop'
            else:
                jobList[3] = 'unknown'
            return jobList
    except paramiko.BadHostKeyException, e:
        raise BadHostKeyError(e.hostname, e.key, e.expected_key)
    except paramiko.AuthenticationException, e:
        raise AuthenticationError()
    except paramiko.SSHException, e:
        raise SCMError(unicode(e))
    except KeyboardInterrupt:
        print("Stopping chaos...")
        sys.exit(0)
    except Exception as inst:
        jobList[2] = 'no response'
        print "dojob error"
        print type(inst)
        print inst.args
        print(inst)
        return jobList
