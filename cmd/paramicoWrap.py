class Paramiko:

	def paramikoWrap(address, command):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(address)
			stdin, stdout, stderr = ssh.exec_command(command)
			resList = []
			for line in stdout.readlines():
				resList.append(i.encode('ascii', 'ignore'))
			return resList 
		except Exception as inst:
			print "generateList error"
			print type(inst)   # the exception instance
			print inst.args     # arguments stored in .args

			

