import random
import sys
import paramiko
import time


class Utility(object):
    @staticmethod
    def getRandomInt(num):
        if num > 0:
            return random.randint(0, num - 1)
        else:
            return -1

    @staticmethod
    def countDown(t):
        if t > 0:
            for i in xrange(t - 1, 0, -1):
                print('Sleep for %s seconds' % str(i))
                sys.stdout.flush()
                time.sleep(1)

    @staticmethod
    def paramikoWrap(address, command):
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
            print "paramikoWrap error"
            print type(inst)
            print inst.args
