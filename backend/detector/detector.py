import datetime, time
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
# from matplotlib import pyplot as plt
# from PIL import Image

from utils import label_map_util
from utils.heatmap import HeatMap
from evaluation.evaluation_helper import write_prediction

from utils import visualization_utils as vis_util
from utils.fileio import clear_files
from utils.args import parse_args
from imutils.video import FPS
import imutils
import cv2
import time

args = parse_args()

if args.videopath:
    VIDEO_INPUT = args.videopath
else:
    VIDEO_INPUT = 0

# ## If you are using a custom TensorFlow model, you will need to update PATH_TO_CKPT (can be any .pb file exported using the `export_inference_graph` tool), PATH_TO_LABELS, and NUM_CLASSES

MODEL_NAME = args.model
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = 'downloaded_models/' + MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

PROCESSING_FRAME_RATE = args.skip_frames + 1

clear_files() # clears data from previous detector instances

if not os.path.exists('downloaded_models'):
    os.makedirs('downloaded_models')

if not os.path.exists('../data'):
    os.makedirs('../data')

if args.save_predictions:
    if not os.path.exists('evaluation/eval-data'):
        os.makedirs('../eval-data')
    if not os.path.exists('evaluation/detection-results'):
        os.makedirs('../detection-results')
    if not os.path.exists('evaluation/images-optional'):
        os.makedirs('../images-optional')

# Download Model
if not os.path.exists('downloaded_models/' + MODEL_NAME + '/frozen_inference_graph.pb'):
    print('Downloading the model')
    opener = urllib.request.URLopener()
    opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, 'downloaded_models/' + MODEL_FILE)
    tar_file = tarfile.open('downloaded_models/' + MODEL_FILE)
    for file in tar_file.getmembers():
        file_name = os.path.basename('downloaded_models/' + file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, os.getcwd() + '/downloaded_models')
    print('Download complete')
else:
    print('Model already exists')

# ## Load a (frozen) Tensorflow model into memory.

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# intializing the web camera device
cap = cv2.VideoCapture(VIDEO_INPUT)
fps = FPS().start()

# write state and records for backend API
state = open('../data/state.txt', 'w+')
with open('../data/records.txt', 'w+') as records:
    records.seek(0)
    records.write('')

# Running the tensorflow session
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        frame = 0
        ret = True
        num_times = 0
        while (ret):
            ret, image_np = cap.read()
            if not ret:
                break
            if frame % PROCESSING_FRAME_RATE == 0:
                if num_times < 10: # update image for first 10 frames (the first few frames tend to be black)
                    cv2.imwrite('../data/camera-image.jpg', image_np)
                    num_times += 1

                if args.save_predictions:
                    cv2.imwrite('evaluation/mAP/input/images-optional/{}.jpg'.format(int(frame/PROCESSING_FRAME_RATE)), image_np)

                # image_np = imutils.resize(image_np, width=200)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
                # t = time.clock()
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})


                if args.save_predictions:
                    write_prediction(int(frame/PROCESSING_FRAME_RATE), np.squeeze(boxes),
                                     np.squeeze(scores),
                                     height=image_np_expanded.shape[1],
                                     width=image_np_expanded.shape[2])

                coordinates = vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)

                # print(coordinates)
                customers_count = len(coordinates)

                now = datetime.datetime.now()
                timestamp = time.time()
                record = '%i  %s\n' % (customers_count, str(now))
                state_record = '%i  %s\n' % (customers_count, str(timestamp))


                # Save records for backend API
                with open('../data/records.txt', 'a+') as records:
                    records.write(record)

                # Store heatmap
                heatmap = HeatMap(width=50, height=30) # width and height define the resolution of the heatmap
                for coordinate in coordinates:
                    heatmap.update(coordinate)
                state.seek(0)
                state.write(state_record)

                # Display image
                cv2.imshow('image', cv2.resize(image_np,
                                                    (int(image_np.shape[1]/2),
                                                    int(image_np.shape[0]/2))))
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    cap.release()
                    break
                fps.update()
            frame += 1
state.close()
