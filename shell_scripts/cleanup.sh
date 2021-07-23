#!/bin/bash

# Figyelmeztetés kiadása
read -n 1 -p "Run this script only after you've ran 'upload.sh', as this will delete every file created by 'retrain.sh'. Press Ctrl+C to cancel."

# Dolgozó mappába való átváltás
cd ~
# Ha létezik az anaconda3 mappa, legyen törölve
[[ -d anaconda3 ]] && rm -rf anaconda3
wait
# Ha létezik az anaconda telepítő fájlja, legyen törölve
[[ -a Anaconda3-4.0.0-Linux-x86_64.sh ]] && rm Anaconda3-4.0.0-Linux-x86_64.sh
wait
# Ha létezik a model_retrain jupyter notebook fájl, legyen törölve
[[ -a model_retrain.ipynb ]] && rm model_retrain.ipynb
wait
# Ha létezik a tensorflow-for-poets-2 mappa, legyen törölve
[[ -d tensorflow-for-poets-2 ]] && rm -rf tensorflow-for-poets-2
wait
# Ha létezik a train_images mappa, legyen törölve
[[ -d train_images ]] && rm -rf train_images
wait

