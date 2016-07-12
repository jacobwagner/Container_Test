import subprocess
import sys
from dataContract.containerState import ContainerState


class LXC:
    shortTimeout = '5'
    longTimeout = '15'

    def start(self, containerName):
        try:
            subprocess.check_call(['lxc-start', '-n', containerName, '--daemon'])
            subprocess.check_call(
                ['lxc-wait', '-n', containerName, '-s', ContainerState.RUNNING, '-t', self.longTimeout])
        except subprocess.CalledProcessError:
            print("wait error")
            raise
        except:
            print("Error", sys.exc_info()[0])
            raise

    def stop(self, containerName):
        try:
            subprocess.check_call(['lxc-stop', '-n', containerName])
            subprocess.check_call(
                ['lxc-wait', '-n', containerName, '-s', ContainerState.STOPPED, '-t', self.longTimeout])
        except subprocess.CalledProcessError:
            print("wait error")
            raise
        except:
            print("Error", sys.exc_info()[0])
            raise

    def freeze(self, containerName):
        try:
            subprocess.check_call(['lxc-freeze', '-n', containerName])
            subprocess.check_call(
                ['lxc-wait', '--name', containerName, '-s', ContainerState.FROZEN, '-t', self.shortTimeout])
            return True
        except subprocess.CalledProcessError:
            print("wait error")
            raise
        except:
            print("Error", sys.exc_info()[0])
            raise

    def unfreeze(self, containerName):
        try:
            st = subprocess.Popen(['lxc-unfreeze', '-n', containerName], stdout=subprocess.PIPE)
            subprocess.check_call(
                ['lxc-wait', '-n', containerName, '-s', ContainerState.RUNNING, '-t', self.shortTimeout])
            return True
        except subprocess.CalledProcessError:
            print("wait error")
            raise
        except:
            print("Error", sys.exc_info()[0])
            raise
