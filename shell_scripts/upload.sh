#!/bin/bash

[[ -d ~/tensorflow-for-poets-2 ]] || echo "Please run 'retrain.sh' before this script."; exit 1;

cd ~/tensorflow-for-poets-2/tf_files

[[ ! -z "$1" ]] && address=$1 || read -p "Please enter the IP address of the Pi you would like to upload this network to: " address

while [[ ! $address =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]] ; do
	read -p "Invalid IP address format. Please try again: " address
done

scp retrained_* pi@"$address":/home/pi
[[ $? -eq 0 ]] && echo "File transferred successfully. Now you can run 'cleanup.sh'."

