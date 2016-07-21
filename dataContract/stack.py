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
import logging

logger = logging.getLogger('chaos')

@Singleton
class Stack(object):
    def __init__(self):
        self.hosts = {}

    def addHost(self, name, component, address, host, ssh_key=None):
        try:
            if not name:
                logger.info("addHost empty name")
                return False
            # host with multiple containers with no component
            if not component and name == host:
                if name not in self.hosts:
                    self.hosts[name] = Host(name, host, address, component, ssh_key)
                else:
                    self.hosts[name].setAddress(address)
                    self.hosts[name].setComponent(component)
                    self.hosts[name].setSshKey(ssh_key)
                return True
            # host has component
            elif component and name == host:
                if name not in self.hosts:
                    self.hosts[name] = Host(name, host, address, component, ssh_key)
                else:
                    self.hosts[name].setAddress(address)
                    self.hosts[name].setComponent(component)
                    self.hosts[name].setSshKey(ssh_key)
                return True
            elif component and name != host:
                if host in self.hosts:
                    self.hosts[host].addToHostDic(Host(name, host, address, component, ssh_key))
                else:
                    self.hosts[host] = Host(host)
                    self.hosts[host].addToHostDic(Host(name, host, address, component, ssh_key))
                return True
            else:
                logger.info("addHost unknown input")
                return False 
        except Exception as inst:
            logger.info('addHost error')
            logger.info(type(inst))
            logger.info(inst.args)
            return False 

    def getRandomInt(self, num):
        if num > 0:
            return random.randint(0, num - 1)
        else:
            return -1

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
            logger.info('getHostList error')
            logger.info(type(inst))
            logger.info(inst.args)
            return []

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
            logger.info("updateServiceState exception")
            logger.info(inst.args)

    def getRandomHost(self):
        try:
            hostList = self.getHostList()
            if len(hostList) != 0:
                index = self.getRandomInt(len(hostList))
                return hostList[index]
        except Exception as inst:
            logger.info('getRandomHost error')
            logger.info(type(inst))
            logger.info(inst.args)
        finally:
            return None

    def updateHostState(self):
        try:
            for host in self.hosts.values():
                if not host.getComponent():
                    stateList = self.getContainerStateList(host.getAddress())
                    for line in stateList:
                        lineSplit = line.split()
                        self.hosts[host.getName()].getHostDic()[lineSplit[0]].setState(lineSplit[1])
        except Exception as inst:
            logger.info("updateContainerState error")
            logger.info(type(inst))
            logger.info(inst.args)
            raise

    def getContainerStateList(self, address):
        try:
            lxcCommand = "/usr/bin/lxc-ls -f | awk '{logger.info($1, $2}'"
            res = self.paramikoWrap(address, lxcCommand)
            return res[2:]
        except Exception as inst:
            logger.info('getContainerState error')
            logger.info(type(inst))
            logger.info(inst.args)
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
            logger.info("generateHostList error")
            logger.info(type(inst))
            logger.info(inst.args)
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
            return []

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
            logger.info("getHostAddress error")
            logger.info(type(inst))
            logger.info(inst.args)

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
                        cmd = 'stop'
                        randomComponent = runningList[index]
                        addressList = serviceDic[randomComponent].keys()
                        address = addressList[self.getRandomInt(len(addressList))]
                    else:
                        logger.info("Doing nothing")
                        continue
                else:
                    index = self.getRandomInt(len(stopList))
                    if index != -1:
                        cmd = 'start'
                        randomComponent = stopList[index]
                        addressList = serviceDic[randomComponent].keys()
                        address = addressList[self.getRandomInt(len(addressList))]
                    else:
                        logger.info("Doing nothing")
                        continue

                for service in dic[randomComponent]:
                    if service != "":
                        jobList.append([address, service, cmd, 'unknown', randomComponent])
                logger.info(jobList)
                #it = pool.imap(doJob, jobList)
  
        except KeyboardInterrupt:
            print("Stopping chaos...")
            sys.exit(0)
        except Exception as inst:
            logger.info("serviceChaos error")
            logger.info(type(inst))
            logger.info(inst.args)
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
            logger.info("serviceChaos error")
            logger.info(type(inst))
            logger.info(inst.args)
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
            logger.info("checkListState error")
            logger.info(type(inst))
            logger.info(inst.args)
            sys.exit(0)

    def containerChaos(self, maximumTime, minimumTime):
        try:
            while 1:
                runningList, stopList = self.generateHostList()
                logger.info('----------------------------------------------------------------------------------------------------------------------------------------------------')
                for i in runningList:
                    logger.info(i.getState() + ' \t ' + i.getName())
                logger.info('----------------------------------------------------------------------------------------------------------------------------------------------------')
                for i in stopList:
                    logger.info(i.getState() + ' \t ' + i.getName())
                logger.info('----------------------------------------------------------------------------------------------------------------------------------------------------')
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
                    logger.info('----------------------------------------------------------------------------------------------------------------------------------------------------')
                self.countDown(t)
        except KeyboardInterrupt:
            print("Stoping chaos...")
            sys.exit(0)
        except Exception as inst:
            logger.info(type(inst))
            logger.info(inst.args)
            logger.info(inst)
            logger.info(time.ctime())
            sys.exit(0)

    def countDown(self, t):
        if t > 0:
            for i in xrange(t - 1, 0, -1):
                print('Sleep for %s seconds' % str(i))
                sys.stdout.flush()
                time.sleep(1)
        else:
            logger.info("error time ", t)
            raise


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
        jobList[3] = 'no response'
        logger.info("dojob error")
        logger.info(type(inst))
        logger.info(inst.args)
        return jobList
