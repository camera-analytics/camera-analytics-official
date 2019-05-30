import sys
from argparse import Namespace, ArgumentParser

def parse_args(args: [str] = None) -> Namespace:
    parser = ArgumentParser(description='Camlytics pedestrian detector')
    parser.add_argument('--videopath', type=str, default=None, help='path to playback video file (default: None)')
    parser.add_argument('--model', type=str, default='ssd_mobilenet_v2_coco_2018_03_29', help='TensorFlow model name from TensorFlow Detection Model Zoo. For the list of TensorFlow Model Zoo out-of-the-box models, see https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md. (default: ssd_mobilenet_v2_coco_2018_03_29)')
    parser.add_argument('--skip-frames', type=int, default=0, help='number of frames to skip. Useful if the frame rate is too high. Note, if --videopath is not set, the detector automatically skips frames if necessary for real time analysis (default: 0)')
    parser.add_argument('--save-predictions', action='store_true', help='save prediction results as txt files along with images in /evaluation/eval-data (default: False)')
    # parser.add_argument('--evaluate', type=str, help='save predictions to txt files in /evaluation/eval-data and, if --videopath is set, evaluate the ')

    if args is None:
        args = sys.argv[1:]
        args = parser.parse_args(args)

    return args
