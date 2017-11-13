#!/bin/bash

if [ $# -eq 0 ] || [ $# -eq 2 ] || [ $# -gt 3 ]; then
	echo "Usage: ocupacio.sh [-g <group> ] MAX_SIZE"
	exit
fi

users=() #Array con los nombres de los usuarios del sistema
user_size=() #Array en el que cada indice contiene el espacio de disco utilizado por el usuario.
it=0 #Iterador de lineas de la salida del comando find
total_size=0

if [ $# -eq 1 ]; then

	max_size=`echo "${1:: -1}"`
	unit_size=`echo "${1: -1}"`

else

	max_size=`echo "${3:: -1}"`
	unit_size=`echo "${3: -1}"`

fi

#Hacemos la conversion de G o M a K

	#El usuario pasa el tamano maximo en MB
	if [ "$unit_size" == "M" ] || [ "$unit_size" == "m" ]; then
		max_size=$(( max_size * 1000 ))
	fi

	#El usuario pasa el tamano maximo en GB
	if [ "$unit_size" == "G" ] || [ "$unit_size" == "g" ]; then
		max_size=$(( max_size * 1000000 ))
	fi

#Arrays con los nombres de usuario y el espacio en disco que ocupa.
for user in `cat /etc/passwd | cut -d ":" -f1`; do
	users+=($user)
	user_size+=(0)
done

if [ $# -eq 1 ]; then
	find_line=`find / -path ./proc -prune -o -type f -exec ls -lh --block-size=K {} \; 2> /dev/null | cut -d ' ' -f3,5`

else

	find_line=`find / -path ./proc -prune -o -type f -group $2 -exec ls -lh --block-size=K {} \; 2> /dev/null | cut -d ' ' -f3,5`

fi

for line in $find_line; do

	#Si el elemento es impar es el nombre del usuario.
	if [ $((it%2)) -eq 0 ]; then

		#Obtenemos el indice del usuario.
		for ((i=0; i<=${#users[@]}; i++)); do

			if [ "${users[$i]}" = "$line" ]; then
				current_user=$i
			fi
		done

	else #Si el elemento es par es el tamano del fichero.

		#Eliminamos la letra del block-size y el espacio entre la unidad y tamano.
		line=`echo ${line//[[:blank:]/} | cut -d 'K' -f1`
		user_size[$current_user]=$(( ${user_size[$current_user]} + line ))
	fi

	it=$(( it + 1 ))
done

# Mostramos los usuarios y cuanto espacio de disco duro han ocupado, si sobrepasan el maximo permitido
# dejaremos un mensaje en el .profile
for ((i=0; i<=${#users[@]}-1; i++)); do

	size=${user_size[i]}
	original_size=${user_size[i]}
 	user=${users[i]}

	#Si el usuario se pasa del maximo permitido le dejamos un mensaje en el .profile
	if [ "$size" -gt "$max_size" ] && [ -d "/home/$user/.profile" ]; then
		profile=`echo /home/$user/.profile`

		echo ' #Para eliminar el mensaje de que estas ocupando demasiado espacio' >> $profile
		echo ' #Debes eliminar las siguientes lineas' >> $profile
		echo ' echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"' >> $profile
		echo ' echo "! AVISO                                                        !"' >> $profile
		echo ' echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"' >> $profile
		echo ' echo "! Has ocupado demasiado espacio, borra o comprime tus ficheros.!"' >> $profile
		echo ' echo "!                                                              !"' >> $profile
		echo ' echo "! Para eliminar este aviso sigue las instrucciones al final    !"' >> $profile
		echo ' echo "! del fichero /home/usuario/.profile                           !"' >> $profile
		echo ' echo "!                                                              !"' >> $profile
		echo ' echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"' >> $profile
		echo ' #Hasta aqui' >> $profile
	fi

	#Pasando a M o G la cantidad de espacio que ocupa cada usuario.
	size_letter="K"

	if [ "${size}" -gt 1000 ]; then
		size=$(( size / 1000 ))
		size_letter="M"
	fi

	if [ "${size}" -gt 1000 ]; then
		size=$(( size / 1000 ))
		size_letter="G"
	fi

	printf '%s %s%s\n' "$user" "$size" "$size_letter"

	if [ $# -eq 3 ]; then
		total_size=$(( total_size + original_size ))
	fi
done

#Mostramos por pantall el espacio ocupado en disco por el grupo pasado como parametro.
if [ $# -eq 3 ]; then

	size_letter="M"
	
	if [ "$total_size" -gt 1000 ]; then
		total_size=$(( total_size / 1000 ))
		size_letter="M"
	fi

	if [ "$total_size" -gt 1000 ]; then
		total_size=$(( total_size / 1000 ))
		size_letter="G"
	fi

	printf 'Espacio total del grupo %s %s%s\n' "$2" "$total_size" "$size_letter"
fi
