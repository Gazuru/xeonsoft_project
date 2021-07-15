import tensorflow as tf
import os

assert tf.__version__.startswith('1.13.1')

IMAGE_SIZE = '160'
MULTIPLIER = '0.50'

ARCHITECTURE = 'mobilenet_' + MULTIPLIER + '_' + IMAGE_SIZE

PATH = 'D:/Python/xeonsoft_project/tensorflow-for-poets-2/'

os.system(
    'python ' + PATH + 'scripts/retrain.py'
    + ' --bottleneck_dir=' + PATH + 'tf_files/bottlenecks'
    + ' --how_many_training_steps=500'
    + ' --model_dir=' + PATH + 'tf_files/models/'
    + ' --summaries_dir=' + PATH + 'tf_files/training_summaries/' + ARCHITECTURE
    + ' --output_graph=' + PATH + 'tf_files/retrained_graph.pb'
    + ' --output_labels=' + PATH + 'tf_files/retrained_labels.txt --architecture=' + ARCHITECTURE
    + ' --image_dir=' + PATH + 'flower_photos')

os.system(PATH + 'bonnet_model_compiler.par --frozen_graph_path=' + PATH + 'tf_files/retrained_graph.pb'
          + ' --output_graph_path=' + PATH + 'tf_files/retrained_graph.binaryproto'
          + ' --input_tensor_name==input --output_tensor_names=final_result --input_tensor_size=160 --debug')
