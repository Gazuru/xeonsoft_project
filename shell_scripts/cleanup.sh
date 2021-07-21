#!/bin/bash

read -n 1 -p "Run this script only after you've ran 'upload.sh', as this will delete every file created by 'retrain.sh'. Press Ctrl+C to cancel."

cd ~
[[ -d anaconda3 ]] && rm -rf anaconda3
wait
[[ -a Anaconda3-4.0.0-Linux-x86_64.sh ]] && rm Anaconda3-4.0.0-Linux-x86_64.sh
wait
[[ -a model_retrain.ipynb ]] && rm model_retrain.ipynb
wait
[[ -d tensorflow-for-poets-2 ]] && rm -rf tensorflow-for-poets-2
wait
[[ -d train_images ]] && rm -rf train_images
wait

