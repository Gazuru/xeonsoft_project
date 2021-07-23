#!/bin/bash

# Dolgozó mappába váltás
cd ~

# Amennyiben nem létezik a train_images mappa, annak, és almappáinak létrehozása, valamint figyelmeztetés, miszerint
# szükséges a mappába helyezni a tanító képeket
if [[ ! -d train_images ]] ; then
       	mkdir -p train_images
       	mkdir -p train_images/correct
	mkdir -p train_images/faulty
	echo "Please place your training images into the corresponding folder inside 'train_images'."
	return
fi
# Annak ellenőrzése, hogy a tanító képek a megfelelő helyen vannak-e
if [[ ! $(ls -A "train_images/correct") ]] || [[ ! $(ls -A "train_images/faulty") ]] ; then
       	echo "The correct and faulty folders are empty. Quitting..."
	return
fi
# Az SSL certificate másolása, ha nem ott van, ahol szükség van rá
if [ ! -d /etc/pki/tls/certs ] && [ ! -a /etc/pki/tls/certs/ca-bundle.crt ] ; then
	sudo mkdir -p /etc/pki/tls/certs
	sudo cp /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt
fi
# Ha nincs telepítve az anaconda, akkor annak telepítése
if [[ -z $(which conda) ]] ; then
	wget -O Anaconda3-4.0.0-Linux-x86_64.sh http://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh
	wait
	bash Anaconda3-4.0.0-Linux-x86_64.sh -b
	wait
fi

wait

# anaconda frissítése
conda update conda -y
wait
# Ha nincs létrehozva a megfelelő virtuális környezet, akkor annak létrehozása
if [[ -z $(conda env list | grep venv_x) ]] ; then
	conda create -n venv_x python=3.6 -y
fi
wait
# Virtuális környezetbe belépés
source activate venv_x
# model_retrain jupyter notebook fájl beszerzése
wget -O model_retrain.ipynb https://raw.githubusercontent.com/Gazuru/xeonsoft_project/master/model_retrain.ipynb
wait
# model_retrain futtatása
ipython -c "%run model_retrain.ipynb"
wait
# Kilépés a virtuális környezetből
source deactivate
# Figyelmeztetés, hogy mostmár futtatható a feltöltés
echo "Run 'upload.sh' to upload retrained graph to Raspberry device."
