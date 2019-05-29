import os
import six.moves.urllib as urllib
import tarfile

""" Generated data file paths """
GENERATED_DATA_DIRECTORY = os.path.join(os.path.dirname(os.getcwd()), 'data')
STATE_FILE = os.path.join(GENERATED_DATA_DIRECTORY, 'state.txt')
RECORDS_FILE = os.path.join(GENERATED_DATA_DIRECTORY, 'records.txt')
POSITIONS_FILE = os.path.join(GENERATED_DATA_DIRECTORY, 'positions-hashed.txt')
IMAGE_FILE = os.path.join(GENERATED_DATA_DIRECTORY, 'camera-image.jpg')

def clear_generated_data_files():
    """ Clears old generated data files """
    if os.path.exists(POSITIONS_FILE):
        os.remove(POSITIONS_FILE)
    if os.path.exists(RECORDS_FILE):
        os.remove(RECORDS_FILE)
    if os.path.exists(RECORDS_FILE):
        os.remove(RECORDS_FILE)

def create_evaluation_folder():
    EVALUATION_DIRECTORY = '../evaluation'
    if not os.path.exists(os.path.join(EVALUATION_DIRECTORY, 'eval-data')):
        os.makedirs(os.path.join(EVALUATION_DIRECTORY, 'eval-data'))
    if not os.path.exists(os.path.join(EVALUATION_DIRECTORY, 'detection-results')):
        os.makedirs(os.path.join(EVALUATION_DIRECTORY, 'detection-results'))
    if not os.path.exists(os.path.join(EVALUATION_DIRECTORY, 'images-optional')):
        os.makedirs(os.path.join(EVALUATION_DIRECTORY, 'images-optional'))

def download_model(model_name, model_directory):
    MODEL_FILE = model_name + '.tar.gz'
    DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    model_directory = 'downloaded_models'
    PATH_TO_CKPT = os.path.join(model_directory, model_name, 'frozen_inference_graph.pb')

    if not os.path.exists(model_directory):
        os.makedirs(model_directory)

    print('Downloading the model')
    opener = urllib.request.URLopener()
    opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, 'downloaded_models/' + MODEL_FILE)
    tar_file = tarfile.open('downloaded_models/' + MODEL_FILE)
    for file in tar_file.getmembers():
        file_name = os.path.basename('downloaded_models/' + file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, os.getcwd() + '/downloaded_models')
    print('Download complete')
