import paramiko
import pprint


class ServiceCheck:
    def checkServiceStatus(self, ip, serviceName, serviceStatus):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip)
        stdin, stdout, stderr = ssh.exec_command(self.getServiceCMD(serviceName, serviceStatus))
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(stdout.readlines())

    def getServiceCMD(self, serviceName, serviceStatus):
        cmd = "/etc/init.d/%s %s" % (serviceName, serviceStatus)
        return cmd
