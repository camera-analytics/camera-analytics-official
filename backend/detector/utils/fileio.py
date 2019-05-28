import os

""" Generated data file names """
GENERATED_DATA_DIRECTORY = os.path.join(os.path.dirname(os.getcwd()), 'data')
STATE_FILE = os.path.join(GENERATED_DATA_DIRECTORY, 'state.txt')
RECORDS_FILE = os.path.join(GENERATED_DATA_DIRECTORY, 'records.txt')
POSITIONS_FILE = os.path.join(GENERATED_DATA_DIRECTORY, 'positions-hashed.txt')
IMAGE_FILE = os.path.join(GENERATED_DATA_DIRECTORY, 'camera-image.jpg')

""" Files used by model """
DATA_DIRECTORY = 'data'
# Sample video file.
SAMPLE_VIDEO = os.path.join(DATA_DIRECTORY, 'sample.mp4')
# List of the strings that is used to add correct label for each box.
MSCOCO_LABELS = os.path.join(DATA_DIRECTORY, 'mscoco_label_map.pbtxt')

""" Model files 
#  Any model exported using the `export_inference_graph.py` tool can be loaded here
# simply by changing `PATH_TO_CKPT` to point to a new .pb file. By default we use
# an "SSD with Mobilenet" model here.
#
# See https://github.com/tensorflow/models/blob/master/object_detection/g3doc/detection_model_zoo.md
# for a list of other models that can be run out-of-the-box with varying speeds
# and accuracies.
"""
MODEL_NAME = 'ssd_mobilenet_v2_coco_2018_03_29'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
# Path to frozen detection graph, that is actually used for the object detection.
MODEL_DIRECTORY = 'downloaded_models'
PATH_TO_TARFILE = os.path.join(MODEL_DIRECTORY, MODEL_FILE)
PATH_TO_CKPT = os.path.join(MODEL_DIRECTORY, MODEL_NAME, 'frozen_inference_graph.pb')


""" Clears old generated data files """
def clear_files():
    if os.path.exists(POSITIONS_FILE):
        os.remove(POSITIONS_FILE)
    if os.path.exists(RECORDS_FILE):
        os.remove(RECORDS_FILE)
    if os.path.exists(RECORDS_FILE):
        os.remove(RECORDS_FILE)
