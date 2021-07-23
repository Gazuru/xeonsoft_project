#!/bin/bash

# A retrain.sh előleges futtatási mivoltjának ellenőrzése
if [[ ! -d ~/tensorflow-for-poets-2 ]] ; then
	echo "Please run 'retrain.sh' before this script."
       	exit 1;
fi
# A szükséges mappába váltás
cd ~/tensorflow-for-poets-2/tf_files
# Ha van megadott argumentum, értékül adás az address változónak, ellenkező esetben felkéri a program, hogy meg legyen
# adva
if [[ ! -z "$1" ]] ; then
       	address=$1 
else
	read -p "Please enter the IP address of the Pi you would like to upload this network to: " address
fi
# Amennyiben nem megfelelő formátumban van megadva az IP-cím, a következő ciklus eléri, hogy a felhasználó kijavítsa
while [[ ! $address =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]] ; do
	read -p "Invalid IP address format. Please try again: " address
done
# A fájl átmásolása
scp retrained_* pi@"$address":/home/pi
# Amennyiben a visszatérési kódja az előző parancsnak 0, sikeresen lefutott a program, futtatható a cleanup.sh
if [[ $? -eq 0 ]] ; then
       	echo "File transferred successfully. Now you can run 'cleanup.sh'."
fi

