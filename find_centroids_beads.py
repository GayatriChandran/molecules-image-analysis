#!/usr/bin/env python
"""
Loads an image and detected peaks in that image. 
Selects an ROI around each detected peak and finds the centroid.

Gayatri 10/19
"""

import numpy
import glob
import datareader
import pandas as pd
from scipy import ndimage

def FindCentroid(roi):
    COM = ndimage.measurements.center_of_mass(roi)
    coordinates = tuple(160*x for x in COM)
    return coordinates

if (__name__ == "__main__"):
    
    # frames = sorted(glob.glob('D:/gayatri-folder/old-blinking-experiments/1-31-Aug-2019-Beads/image-analysis/frame_*.tif'))

    movie_file = 'D:/gayatri-folder/old-blinking-experiments/1-31-Aug-2019-Beads/image-analysis/frame_0001.tif'
    movie = datareader.inferReader(movie_file)
    frame = movie.loadAFrame(0)

    peaks = pd.read_csv('D:/gayatri-folder/old-blinking-experiments/1-31-Aug-2019-Beads/image-analysis/peaks_0001.csv')

    rows = peaks['row']
    columns = peaks['col']
    x = peaks['x']
    y = peaks['y']
    print('Array position : ', rows[46], columns[46])
    roi = frame[(rows[46]-1):(rows[46]+2), (columns[46]-1):(columns[46]+2)]
    COM = ndimage.measurements.center_of_mass(roi)
    coordinates = tuple(160*x for x in COM)
    centroid = (((x[46]-1)*160)+coordinates[0], ((y[46]-1)*160)+coordinates[1])
    print('Centroid : ', centroid)

        
    
