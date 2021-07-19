#!/bin/bash

cd ~

if [[ ! -d train_images ]] ; then
       	mkdir -p train_images
       	mkdir -p train_images/correct
	mkdir -p train_images/faulty
	echo "Please place your training images into the corresponding folder inside 'train_images'."
	return
fi

if [[ ! $(ls -A "train_images/correct") ]] || [[ ! $(ls -A "train_images/faulty") ]] ; then
       	echo "The correct and faulty folders are empty. Quitting..."
	return
fi

if [ ! -d /etc/pki/tls/certs ] && [ ! -a /etc/pki/tls/certs/ca-bundle.crt ] ; then
	sudo mkdir -p /etc/pki/tls/certs
	sudo cp /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt
fi

if [[ -z $(which conda) ]] ; then
	wget -O Anaconda3-4.0.0-Linux-x86_64.sh http://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh
	wait
	bash Anaconda3-4.0.0-Linux-x86_64.sh -b
	wait
fi

wait

conda update conda -y
wait
if [[ -z $(conda env list | grep venv_x) ]] ; then
	conda create -n venv_x python=3.6 -y
fi
wait
source activate venv_x
wget -O model_retrain.ipynb https://raw.githubusercontent.com/Gazuru/xeonsoft_project/master/model_retrain.ipynb
wait
ipython -c "%run model_retrain.ipynb"
wait
source deactivate
echo "Run 'upload.sh' to upload retrained graph to Raspberry device."
