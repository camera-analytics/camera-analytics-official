import datetime, time
import numpy as np
import os
import tarfile
import tensorflow as tf
import cv2

from utils import label_map_util
from utils.heatmap import HeatMap
from evaluation.evaluation_helper import write_prediction

from utils import visualization_utils as vis_util
from utils.fileio import clear_generated_data_files, create_evaluation_folder, download_model, GENERATED_DATA_DIRECTORY, STATE_FILE, RECORDS_FILE, POSITIONS_FILE, IMAGE_FILE
from utils.args import parse_args
from imutils.video import FPS

def main(args):
    if args.videopath:
        # Use playback video file.
        VIDEO_INPUT = args.videopath
    else:
        # Use webcam.
        VIDEO_INPUT = 0

    # Download model if not downloaded.
    MODEL_DIRECTORY = 'downloaded_models'
    MODEL_NAME = args.model
    PATH_TO_CKPT = os.path.join(MODEL_DIRECTORY, MODEL_NAME, 'frozen_inference_graph.pb')
    if not os.path.exists(os.path.join(MODEL_DIRECTORY, MODEL_NAME, 'frozen_inference_graph.pb')):
        download_model(model_name=MODEL_NAME, model_directory=MODEL_DIRECTORY)
    else:
        print('Model already exists')

    if args.save_predictions:
        create_evaluation_folder()

    # Set up data directory, clear old generated data files.
    clear_generated_data_files()
    if not os.path.exists(GENERATED_DATA_DIRECTORY):
        os.makedirs(GENERATED_DATA_DIRECTORY)

    MSCOCO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

    # Number of label classes (default is MSCOCO's 90 classes)
    NUM_CLASSES = 90

    PROCESSING_FRAME_RATE = args.skip_frames + 1

    # Load a (frozen) Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    # Load label map which maps label indices to category names.
    label_map = label_map_util.load_labelmap(MSCOCO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Intialize the video capture.
    cap = cv2.VideoCapture(VIDEO_INPUT)
    fps = FPS().start()

    # Write state and records for backend API.
    state = open(STATE_FILE, 'w+')
    with open(RECORDS_FILE, 'w+') as records:
        records.seek(0)
        records.write('')

    # Run the tensorflow session.
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            frame = 0
            has_next = True
            num_times = 0
            while (has_next):
                has_next, image_np = cap.read()
                if not has_next:
                    break

                # Process every few frames.
                if frame % PROCESSING_FRAME_RATE == 0:

                    # Update image for first 10 frames (the first few frames tend to be black).
                    if num_times < 10:
                        # Store image for heat map.
                        cv2.imwrite(IMAGE_FILE, image_np)
                        num_times += 1

                    if args.save_predictions:
                        cv2.imwrite('evaluation/eval-data/images-optional/{}.jpg'.format(int(frame/PROCESSING_FRAME_RATE)), image_np)

                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

                    # Each box represents a part of the image where a particular object was detected.
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

                    # Each score represent how level of confidence for each of the objects. Score is shown on the result image, together with the class label.
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                    # Actual detection.
                    (boxes, scores, classes, num_detections) =\
                        sess.run([boxes, scores, classes, num_detections],
                                 feed_dict={image_tensor: image_np_expanded})


                    if args.save_predictions:
                        write_prediction(int(frame/PROCESSING_FRAME_RATE), np.squeeze(boxes),
                                         np.squeeze(scores),
                                         height=image_np_expanded.shape[1],
                                         width=image_np_expanded.shape[2])

                    # Visualization of the bounding boxes.
                    coordinates = vis_util.visualize_boxes_and_labels_on_image_array(
                        image_np,
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
                    # Store heatmap. width and height define the resolution of the heatmap
                    heatmap = HeatMap(width=50, height=30)
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

if __name__ == '__main__':
    args = parse_args()
    main(args)
