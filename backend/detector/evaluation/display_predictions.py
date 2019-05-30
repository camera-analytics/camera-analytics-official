"""
Display bounding boxes on the screen of the ground-truth labels located
in `evaluation/eval-data/ground-truth` and the detection labels located in
`evaluation/eval-data/detection-results`. It uses the images provided in
`evaluation/eval-data/images`.

Assuming files are number 0.txt, 1.txt, 2.txt, ..., change NUM_IMAGES to the
number of the number of images to evaluate.
"""

import numpy as np
import cv2

# TODO: change NUM_IMAGES
NUM_IMAGES = 600
PATH = 'eval-data/'

def get_data(folder, i):
    data = []
    if folder == 'detection-results':
        start_position = 2
    else:
        start_position = 1
        i*=2

    with open('{}{}/{}.txt'.format(PATH, folder, i), 'r') as f:
        for line in f:
            temp_data = [int(float(x)) for x in f.readline().split(' ')[start_position:]]
            if temp_data != []:
                data.append(temp_data)
    return data

# loop over the example detections
for i in range(NUM_IMAGES):
    # load the image
    image = cv2.imread('{}images/{}.jpg'.format(PATH, i))

    # load data
    detection_data = get_data('detection-results', i)
    groundtruth_data = get_data('ground-truth', i)

	# draw the ground-truth bounding box along with the predicted
	# bounding box
    print(detection_data)
    for data in detection_data:
        cv2.rectangle(image, (data[0], data[1]),
        	(data[2], data[3]), (0, 255, 0), 2)
    for data in groundtruth_data:
        cv2.rectangle(image, tuple(data[0:2]),
        	tuple(data[2:4]), (0, 0, 255), 2)
    # show the output image
    cv2.imshow("Image", cv2.resize(image,
                                        (int(image.shape[1]/2),
                                        int(image.shape[0]/2))))
    cv2.waitKey(0)
