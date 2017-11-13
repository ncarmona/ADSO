import string
import os
import datetime
from os import stat, path
from pwd import getpwuid
import re

class libadso:

	#Obtiene el nombre de todos los usuarios del sistema.
	def getusers(self):
		passwd=open('/etc/passwd')
		users=[]

		for userline in passwd:
			userinfo=userline.split(':')
			users.append(userinfo[0])
			
		return users

	#Obtiene el nombre de todos los groups del sistema.
	def getgroups(self):
		grouparr=[]
		groups=open('/etc/group')
		for group in groups:		
			grouparr.append(group.split(':')[0])

		return grouparr

	#Obtiene informacion sobre el usuario 
	def getuser(self,user):
		passwd=open('/etc/passwd')
		for userline in passwd:
			userinfo=userline.split(':')
			if userinfo[0]==user:
				return userinfo
				
	#Obtiene informacion del fichero, propietario, fecha de creación, fecha de modificación, tamaño y ruta absoluta.
	def fileinfo(self,file):
		data = []

		data.append(getpwuid(stat(file).st_uid).pw_name)
		data.append(getpwuid(stat(file).st_uid).pw_uid)
		data.append(getpwuid(stat(file).st_uid).pw_gid)
		data.append(datetime.datetime.fromtimestamp(os.stat(file).st_ctime).strftime("%Y-%m-%d %H:%M:%S"))
		data.append(datetime.datetime.fromtimestamp(os.stat(file).st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
		data.append(os.stat(file).st_size)

		groups=open('/etc/group')
		for group in groups:
			group=group.split(':')
			if group[2] == str(data[2]):
				data.append(group[0])

		return data

	#Devuelve cuantos procesos hay en el sistema.
	def countproc(self,user='*'):
		numproc=0

		if user == '*': #Procesos de todos los usuarios.
			for root, dirs, files in os.walk("/proc"):
				path = root.split(os.sep)
				if os.path.basename(root).isdigit() and ((len(path) -1) == 2):	
					numproc+=1

		else: #Procesos del usuario user
			for root, dirs, files in os.walk("/proc"):
				path = root.split(os.sep)
				if os.path.basename(root).isdigit() and ((len(path) -1) == 2):
					print(os.path.join(root))

					#Abrimos el fichero que contiene informacion del proceso.
					status=open(os.path.join(root)+"/status")
					for line in status:
						if line.startswith('Uid:'):
							line=re.split(r'\t+', line)
							userpid=self.getuser(user)[2]
							if userpid == line[2]:
								numproc+=1
		return numproc
	#Devuelve una lista con las interfaces de red activas.
	def netinterfaces(self):
		interfaces=open('/etc/network/interfaces')
		interfacesArray=[]

		for line in interfaces:
			if line.startswith("iface"):
				line=line.split(" ")
				interfacesArray.append(line[1])

		return interfacesArray
