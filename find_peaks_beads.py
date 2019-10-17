#!/usr/bin/env python
"""
Loads one frame of a dax movie, in which fluorophores are not activated.
Finds background median value from that.
Loads another frame of the movie that contains emitting molecules.
Finds local maxima in the data, selects only those peaks which are twice the background value.
And then, it find average peak intensity.

Gayatri 10/19
"""

import numpy
import glob
import datareader
import sys
import matplotlib.pyplot as plt
import pandas as pd
import tifffile

if (__name__ == "__main__"):
    
    # if (len(sys.argv) != 2):
    #     print("usage: <movie>")
    #     exit()

    dax_files = sorted(glob.glob('D:/gayatri-folder/old-blinking-experiments/1-31-Aug-2019-Beads/beads_647_*.dax'))
    output_directory = 'D:/gayatri-folder/old-blinking-experiments/1-31-Aug-2019-Beads/image-analysis/'
    for movie_file in dax_files:
        # print(movie_file)
        # Load first frame of movie, using command : python find_peaks_beads.py D:\gayatri-folder\old-blinking-experiments\1-31-Aug-2019-Beads\beads_647_0001.dax
        movie = datareader.inferReader(movie_file)
        frame = movie.loadAFrame(1)
        index = movie_file.rsplit('.dax', 1)[0][-4:]
        with tifffile.TiffWriter(output_directory + "frame_" + index + ".tif") as tf:
            tf.save(frame)
        # print('Saved frame_0001.csv')
        peaks = []
        noise_median = 100 # This is ideally calculated from a frame with shutter closed. Or, I think, with fluorophores switched off. I have neither. So let's assume 100.
        # Select 8-neighbourhoods and check if middle elements qualify as local maxima. Save detected peaks.
        for x in range(254) :
            for y in range(254) :
                neighbours=[]
                for i in range(3) :
                    for j in range(3) :
                        neighbours.append(frame[x+i][y+j])
                maxpos = neighbours.index(max(neighbours))

                # Save detected peaks.
                if maxpos == 4 and max(neighbours)>=noise_median*2:
                    peaks.append([x+1,y+1,y+2,x+2,max(neighbours),numpy.around(numpy.mean(neighbours),decimals=3)])
                    
        # with tifffile.TiffWriter("localmaxima.tif") as tf:
        #         tf.save(mask)

        # Save positions of peaks and also display mean peak intensity
        df = pd.DataFrame(peaks, columns=['row','col','x','y','peak','avg'])
        df.to_csv(output_directory + "peaks_" + index + ".csv", header=['row','col','x','y','peak','avg'],index=False)
        mean_peak = df['avg'].mean()
        # print("Mean peak intensity = ", mean_peak)
        median_peak = df['avg'].median()
        # print("Median peak intensity = ", median_peak)
        info= open(output_directory + "info_" + index + ".txt","w+")
        info.write('Average molecule intensity :' + str(mean_peak))
        info.write('\n')
        info.write('Median : ' + str(median_peak))
        info.close()
