#!/bin/bash

if [[ ! -d ~/tensorflow-for-poets-2 ]] ; then
	echo "Please run 'retrain.sh' before this script."
       	exit 1;
fi

cd ~/tensorflow-for-poets-2/tf_files

if [[ ! -z "$1" ]] ; then
       	address=$1 
else
	read -p "Please enter the IP address of the Pi you would like to upload this network to: " address
fi

while [[ ! $address =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]] ; do
	read -p "Invalid IP address format. Please try again: " address
done

scp retrained_* pi@"$address":/home/pi
if [[ $? -eq 0 ]] ; then
       	echo "File transferred successfully. Now you can run 'cleanup.sh'."
fi

