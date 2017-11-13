#!/usr/bin/python3

from libadso import libadso
import sys
import os

#El numero de parametros debe ser 1 o 3
if len(sys.argv[1:]) == 0 or len(sys.argv[1:]) > 3 or len(sys.argv[1:]) == 2:
    exit("Usage: ocupacio.sh [-g <group> ] MAX_SIZE")

#Si solo hay un parametro debe especificar el tamano maximo.
if sys.argv[1] == "-g" and len(sys.argv[1:]) == 1:
    exit("Usage: ocupacio.sh [-g <group> ] MAX_SIZE")

adso = libadso()

#Vector con los usuarios

users=[]
for user in adso.getusers():
	users.append([user , 0])

"""
Obtenemos el maximo de espacio, separamos la letra del numero.
"""

#Letra
if len(sys.argv[1:]) == 1:
	letter_size=sys.argv[1][-1:]
else:
	letter_size=sys.argv[3][-1:]

#Numeros
if len(sys.argv[1:]) == 1:
	size=sys.argv[1][:-1]
else:
	size=sys.argv[3][:-1]

#Pasamos el maximo a bytes.
param_size=0
if letter_size == "K":
	param_size*=1000
if letter_size == "M":
	param_size*=1000000
if letter_size == "G":
	param_size*=1000000000

#Recorremos el disco desde la raiz, obtenemos el tamano de cada fichero, su usuario y grupo.
for root, dirs, files in os.walk("/"):
	path = root.split(os.sep)
	for file in files:
		try:
			username=adso.fileinfo(os.path.join(root, file))[0]
			size=adso.fileinfo(os.path.join(root, file))[5]
			groupname=adso.fileinfo(os.path.join(root, file))[6]

			#Buscamos el usuario y le sumamos size
			for user in users:
				if user[0] == username and len(sys.argv[1:]) == 1:
					user[1]+= size
				if len(sys.argv[1:]) == 3 and groupname == sys.argv[2] and user[0] == username:
					user[1]+= size
		except FileNotFoundError:
			pass
#Mostramos el vector con los usuarios y cuanto espacio ocupan en disco.
for user in users:
	#Asignamos la unidad mas adecuada para el tamano (B, K, M o G)

	letra = "B"
	tam = round(user[1],2)

	if tam > 1000:
		letra="K"
		tam = round(tam/1000,2)
	if tam > 1000:
		letra="M"
		tam = round(tam/1000,2)
	if tam > 1000:
		letra="G"
		tam = round(tam/1000,2)

	print(user[0]+'  '+str(tam)+letra)

	#Si el usuario tiene ocupado mas espacio del permitido le dejamos un mensaje en el .profile
	if tam > param_size:
		try:
			profile=open('/home/'+user[0]+"/.profile", 'a')
			profile.write("#Para eliminar el mensaje de que estas ocupando demasiado espacio\n")
			profile.write("#Debes eliminar las siguientes lineas\n")
			profile.write('echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"\n')
			profile.write('echo "! AVISO                                                        !"\n')
			profile.write('echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"\n')
			profile.write('echo "! Has ocupado demasiado espacio, borra o comprime tus ficheros.!"\n')
			profile.write(' echo "!                                                              !"\n')
			profile.write('echo "! Para eliminar este aviso sigue las instrucciones al final    !"\n')
			profile.write('echo "! del fichero /home/usuario/.profile                           !"\n')
			profile.write('echo "!                                                              !"\n')
			profile.write('echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"\n')
		except FileNotFoundError:
			pass

