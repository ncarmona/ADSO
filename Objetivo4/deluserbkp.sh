#!/bin/bash

#Comprobamos que los parametros de entrada son correcto.
if [ $# -ne 1 ]; then
	echo "Usage: deluserbkp.sh <user>"
	exit 1
fi

#Bloqueamos el acceso al usuario pasado por parametro.
chsh -s /usr/local/lib/no-login prueba
echo "Se ha bloqueado el acceso al usuario $1"

#Creamos la carpeta de backups si no existe.
if [ ! -d "$HOME/backups" ]; then
	mkdir "$HOME/backups"
	echo "Se ha creado el directorio de backups."
fi

#Obtenemos el directorio home del usuario.
home_dir=`cat /etc/passwd | grep "^$1\>" | cut -d":" -f6`

#Hacemos una copia del directorio home y luego lo borramos.
if [ -d "$home_dir" ]; then

	bkp_path="$HOME/backups/$1_$(date '+%d-%m-%Y').tar.gz"
	tar -zcvf $bkp_path $home_dir
	rm -r $home_dir
	echo "Se ha guardado una copia del home de $1 en $bkp_path"
else
	echo "No se ha hecho una copia de $home_dir, el directorio no existe."
fi

#Buscamos en el sistema los ficheros del usuario pasados por parametro y los eleminamos.
find / -user $1 -exec rm -r "{}" \; 2> /dev/null

echo "Se han borrado ficheros de $1 que estaban fuera de su home."
