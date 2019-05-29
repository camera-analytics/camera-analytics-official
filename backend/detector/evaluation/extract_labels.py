"""
Converts .top groundtruth file into a series of files formatted so that
evluation metrics can be easily obtained.
"""

import numpy as np

from evaluation_helper import write_groundtruth

path = 'TownCentre-groundtruth.top.txt'
data_arr = np.loadtxt(path, delimiter=",")

for row in data_arr:
    frame = int(row[1])
    body_left = row[8]
    body_top = row[9]
    body_right = row[10]
    body_bottom = row[11]
    write_groundtruth(frame, (body_left, body_top, body_right, body_bottom))
