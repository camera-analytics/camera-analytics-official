import datetime, time
import numpy as np
import os
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
from imutils.video import FPS
import cv2

from utils import label_map_util
from utils.visualization_utils import visualize_boxes_and_labels_on_image_array
from utils.heatmap import HeatMap
from utils.fileio import *

# To use the computer webcam, set VIDEO_INPUT = 0
VIDEO_INPUT = SAMPLE_VIDEO

# Constants for processing video.
NUM_CLASSES = 90
PROCESSING_FRAME_RATE = 5

def main():
    # Set up data directory, clear old generated data files.
    clear_files()
    if not os.path.exists(GENERATED_DATA_DIRECTORY):
        os.makedirs(GENERATED_DATA_DIRECTORY)

    # Download model
    if not os.path.exists(MODEL_DIRECTORY):
        os.makedirs(MODEL_DIRECTORY)
    if not os.path.exists(PATH_TO_CKPT):
        opener = urllib.request.URLopener()
        opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, PATH_TO_TARFILE)
        tar_file = tarfile.open(PATH_TO_TARFILE)
        for file in tar_file.getmembers():
            file_name = os.path.basename(os.path.join(MODEL_DIRECTORY, file.name))
            if 'frozen_inference_graph.pb' in file_name:
                tar_file.extract(file, os.path.join(os.getcwd(), MODEL_DIRECTORY))
        print('Download complete')
    else:
        print('Model already exists')

    # Load a (frozen) tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    # Label maps map indices to category names.
    label_map = label_map_util.load_labelmap(MSCOCO_LABELS)
    categories =\
        label_map_util.convert_label_map_to_categories(label_map,
                                                       max_num_classes=NUM_CLASSES,
                                                       use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Initialize the video capture.
    cap = cv2.VideoCapture(VIDEO_INPUT)
    fps = FPS().start()

    # Open the data files.
    state = open(STATE_FILE, 'w+')
    with open(RECORDS_FILE, 'w+') as records:
        records.seek(0)
        records.write('')

    # Run the tensorflow session
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            frame = 0
            has_next = True
            num_image_stored = 0

            while True:
                # Check if video stream has next image.
                has_next, image = cap.read()
                if not has_next:
                    break

                # Process every few frames.
                if frame % PROCESSING_FRAME_RATE == 0:

                    # Store image for heat map.
                    if num_image_stored < 10:
                        cv2.imwrite(IMAGE_FILE, image)
                        num_image_stored += 1

                    # Expand dimensions since the model expects images to have
                    # shape: [1, None, None, 3]
                    image_expanded = np.expand_dims(image, axis=0)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    # Each box represents a part of the image where a particular object was detected.
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    # Each score represent how level of confidence for each of the objects.
                    # The score is shown on the result image, together with the class label.
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                    # Actual detection.
                    (boxes, scores, classes, num_detections) =\
                        sess.run([boxes, scores, classes, num_detections],
                                 feed_dict={image_tensor: image_expanded})

                    # Visualization of the bounding boxes.
                    coordinates = visualize_boxes_and_labels_on_image_array(
                        image,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8)

                    # Store information for frontend.
                    customers_count = len(coordinates)
                    now = datetime.datetime.now()
                    timestamp = time.time()
                    record = '%i  %s\n' % (customers_count, str(now))
                    state_record = '%i  %s\n' % (customers_count, str(timestamp))
                    with open(RECORDS_FILE, 'a+') as records:
                        records.write(record)
                    heatmap = HeatMap(width=50, height=30)
                    for coordinate in coordinates:
                        heatmap.update(coordinate)
                    state.seek(0)
                    state.write(state_record)

                    # Display image.
                    cv2.imshow('image',
                               cv2.resize(image, (int(image.shape[1]/2),
                                                  int(image.shape[0]/2))))
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        cap.release()
                        break
                    fps.update()
                frame += 1
    state.close()

if __name__ == '__main__':
    main()
