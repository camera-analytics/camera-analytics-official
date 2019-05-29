import numpy as np

def _round(x):
    return max(0, int(x-1e-8))

def write_groundtruth(frame, positions):
    """
    Write groundtruth data to a txt file to compare with detector.
    positions:  tuple of ints/floats (left, top, right, bottom) representing the
                position of the bounding box
    """
    with open("mAP/input/ground-truth/{}.txt".format(frame), "a") as f:
        left, top, right, bottom = positions
        f.write('person {} {} {} {}\n'.format(left, top, right, bottom))

def write_prediction(frame, boxes, scores, height, width):
    """
    Write predictions to a txt file to evaluate the performance.
    boxes:  list of positions. Each position is a tuple of ints/floats
            (left, top, right, bottom) representing the position of the bounding
            box
    scores: list of confidence scores (list of floats)
    width:  image width (pixels)
    height: image height (pixels)
    """
    for positions, score in zip(boxes, scores):
        if np.any(positions != 0):
            with open("evaluation/mAP/input/detection-results/{}.txt".format(frame), "a") as f:
                top, left, bottom, right = positions
                left *= width
                right *= width
                top *= height
                bottom *= height
                f.write('person {} {} {} {} {}\n'.format(score, _round(left),
                                                         _round(top),
                                                         _round(right),
                                                         _round(bottom)))
