#!/usr/bin/env python
"""
Loads an image and detected peaks in that image. 
Does least squares fitting of a gaussian function on the roi around each peak.

Gayatri 10/19
"""

import numpy
import glob
import datareader
import pandas as pd
import gaussfit


if (__name__ == "__main__"):

    output_directory = 'D:/gayatri-folder/old-blinking-experiments/1-31-Aug-2019-Beads/image-analysis/'
    tif_files = sorted(glob.glob('D:/gayatri-folder/old-blinking-experiments/1-31-Aug-2019-Beads/image-analysis/frame_*.tif'))
    for movie_file in tif_files:

        # movie_file = 'D:/gayatri-folder/old-blinking-experiments/1-31-Aug-2019-Beads/image-analysis/frame_0001.tif'
        movie = datareader.inferReader(movie_file)
        frame = movie.loadAFrame(0)
        index = movie_file.rsplit('.tif', 1)[0][-4:]


        peaks = pd.read_csv(output_directory + "peaks_" + index + ".csv")

        molecules = pd.DataFrame([], columns=['x','y'])
        k=0
        for i,j in peaks.iterrows():
            print(j[1])
            roi = frame[(j[0]-2):(j[0]+3), (j[1]-2):(j[1]+3)]
            result, good = gaussfit.fitSymmetricGaussian(roi, 1.0)
            print(result)
            if good:
                locs = (result[2], result[3])
                coordinates = tuple(160*x for x in locs)
                localization = (((j[2]-1)*160)+coordinates[0], ((j[3]-1)*160)+coordinates[1])
                molecules.loc[k] = [localization[0], localization[1]]
                k+=1
            else:
                molecules.loc[k] = [numpy.NaN, numpy.NaN]
                k+=1
        
        molecules.to_csv(output_directory + "molecules_" + index + ".csv", header=['x','y'],index=False)
