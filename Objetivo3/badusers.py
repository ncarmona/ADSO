#!/usr/bin/python3

from libadso import libadso
import sys
import os
from datetime import *
import time


#El numero de parametros no debe de ser mayor que 2.
if len(sys.argv[1:]) > 2:
    exit("Usage: badusers.sh [-t <days> ] | [-p]")

#Si solo hay un parametro debe especificar el tiempo maximo.
if len(sys.argv[1:]) == 2 and sys.argv[1] != "-t":
	exit("Usage: badusers.sh [-t <days> ] | [-p]")

#Obtiene el numero de dias pasados como parametro y la fecha actual.
if len(sys.argv[1:]) == 2 and sys.argv[1] == "-t":
	days=int(sys.argv[2][:-1])

today=time.strftime("%Y-%m-%d %H:%M:%S")
today_date=today.split(' ')[0].split('-')
today_time=today.split(' ')[1].split(':')

today=datetime(int(today_date[0]), int(today_date[1]), int(today_date[2]),int(today_time[0]), int(today_time[1]), int(today_time[2]))

adso = libadso()

for user in adso.getusers():
	userinfo = adso.getuser(user)
	home = userinfo[5]
	if os.path.exists(home):
		# -t nd
		if len(sys.argv[1:]) == 2:
			
			for root, dirs, files in os.walk(home):
				path = root.split(os.sep)
				count_mtime_inv_files=0
				"""
				Para que un usuario sea valido debe haber modificado alguno de sus
				ficheros del home en los ultimos days dias.
				"""
				for file in files:
					try:
						#Ruta completa del fichero.
						filepath=os.path.join(root, file)
						
						"""							
						Obtenemos la fecha de modificacion del fichero y
						la pasamos a un datetime para poder calcular la
						diferencia entre la fecha de modificacion y la
						fecha actual.
						"""
						fileinfo=adso.fileinfo(filepath)

						mtime_date=fileinfo[4].split(' ')[0].split('-')
						mtime_time=fileinfo[4].split(' ')[1].split(':')
						mtime=datetime(int(mtime_date[0]), int(mtime_date[1]), int(mtime_date[2]),int(mtime_time[0]), int(mtime_time[1]), int(mtime_time[2]))

						diff=(today-mtime).days
			
						"""
						Si encontramos un fichero cuya fecha de modificacion
						sea menor a la diferencia de dias el usuario sera
						valido.
						"""
						if diff > days:
							count_mtime_inv_files+=1
					except FileNotFoundError:
						pass
			if count_mtime_inv_files > 0:
				print(user)		
					
		#-p
		elif len(sys.argv[1:]) == 1:
			#Si el numero de procesos del usuario es 0 este sera invalido.
			if adso.countproc(user) == 0:	
				print(user)
		#noparam
		else:
			invalid=True

			for root, dirs, files in os.walk(home):
				
				for file in files:
					try:
						filepath=os.path.join(root, file)
						if adso.fileinfo(filepath)[0] == user:
							invalid=False
					except FileNotFoundError:
						pass
			if invalid:
				print(user)
	else:
		print(user)
