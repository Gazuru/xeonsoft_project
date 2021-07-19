#!/bin/bash

read -n 1 -p "Run this script only after you've ran 'upload.sh', as this will delete every file created by 'retrain.sh'. Press Ctrl+C to cancel."

cd ~

rm -rf anaconda3
wait
rm Anaconda3-4.0.0-Linux-x86_64.sh
wait
rm model_retrain.ipynb
wait
rm -rf tensorflow-for-poets2
wait
rm -rf train_images
wait

