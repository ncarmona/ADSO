#!/bin/bash
p=0
usage="Usage: BadUser.sh [-p]"
#Detecció de opcions d'entrada: només son vàlids: sense paràmetres i -p
if [ $# -ne 0 ]; then
	if [ $# -eq 1 ]; then
		if [ $1 == "-p" ]; then
			p=1
		else
			echo $usage; exit 1
		fi
#	else
#		echo $usage; exit 1
	fi

#Anadido para la segunda parte del script 1
	if [ $# -eq 2 ]; then
		if [ $1 == "-t" ]; then
			hours=`echo "${2:: -1}"`
			hours=$(( hours * 24 ))			
		else
			echo $usage; exit 1
		fi
	fi
#Anadido para la segunda parte del script 1
fi

#Afegiu una comanda per llegir el fitxer de password i només agafar el camp de nom de l'usuari

for user in `cut -d: -f1 /etc/passwd`; do #En cada iteracion leemos el nombre del usuario del fichero /etc/passwd

	home=`cat /etc/passwd | grep "^$user\>" | cut -d: -f6` #Obtiene la ruta del home del usuario $user

	if [ -d $home ]; then #Comprueba si el directorio home del usuario $user existe
		if [ $# -eq 2 ]; then #Si se ejecuta con el parametro -t
			#Si el numero de ficheros y veces que $user se han logeado es > 1 no se anaden a la lista de badusers.
			num_fich=`find $home -type f -user $user -mtime +$hours 2> /dev/null | wc -l`
			logged=`last -$2 | grep $user | wc -l`
			
			if [ $num_fich -gt 0 ] && [ $logged -gt 0 ]; then
				num_fich=1
			else
				num_fich=0
			fi

		else #Ejecucion con el parametro -p
			num_fich=`find $home -type f -user $user 2> /dev/null | wc -l`
		fi
	else
		num_fich=0
	fi


	if [ $num_fich -eq 0 ]; then
		if [ $p -eq 1 ]; then
		#Afegiu una comanda per detectar si l'usuari te processos en execució, si no te
		#ningú la variable $user_proc ha de ser 0
		user_proc=`ps -ef | cut -d ' ' -f1 | grep -c $user`

			if [ $user_proc -eq 0 ]; then
				echo "$user"
			fi
		else
			echo "$user"
		fi
	fi
done

