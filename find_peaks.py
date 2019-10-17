#!/usr/bin/env python
"""
Loads one frame of a dax movie, in which fluorophores are not activated.
Finds background median value from that.
Loads another frame of the movie that contains emitting molecules.
Finds local maxima in the data, selects only those peaks which are twice the background value.
And then, average peak intensity is found.

Gayatri 10/19
"""

import numpy
import datareader
import sys
import matplotlib.pyplot as plt
import pandas as pd

if (__name__ == "__main__"):
    
    if (len(sys.argv) != 2):
        print("usage: <movie>")
        exit()

    # Load first frame of movie, in which there is only background noise
    movie = datareader.inferReader(sys.argv[1], verbose = True)
    print("Loaded first frame of movie, with mostly only background noise...")
    bg = movie.loadAFrame(0)
    numpy.save('background', bg)

    # Find median of backgrounf
    noise_median = numpy.median(bg, axis=None)
    print("Median of background = ", noise_median)
    noise_mean = numpy.mean(bg, axis=None)

    # Save a graph showing background intensity distribution, just for fun
    BG = bg.flatten()
    plt.hist(BG, bins=15, color='grey')
    plt.title('Background intensity distribution')
    plt.ylabel('Frequency')
    plt.xlabel('Pixel intensity')
    plt.text(104, 14000, r'Mean =' + str(numpy.around(noise_mean, 2)), fontsize=10)
    plt.text(104, 13000, r'Median =' + str(noise_median), fontsize=10)
    plt.savefig('bg.png')

    # print('Saved bg.png in same directory, graph showing spread of background pixel values.')
    # print('Loaded dax movie frame with some fluorophores switched on...')

    # Load the next dax movie frame with fluorescent molecules in it
    frame = movie.loadAFrame(1)
    numpy.save('dax-frame', frame)
    peaks = []

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
                peaks.append([x+1,y+1,y+2,x+2,max(neighbours)])

    # with tifffile.TiffWriter("localmaxima.tif") as tf:
    #         tf.save(mask)

    # Save positions of peaks and also display mean peak intensity
    df = pd.DataFrame(peaks, columns=['row','col','x','y','value'])
    df.to_csv("peaks.csv", header=['row','col','x','y','value'],index=False)
    print('Saved peaks.csv, contains locations of local maxima and peak values')
    peaks1 = pd.read_csv("peaks.csv")
    mean_peak_intensity = df['value'].mean()
    print("Mean peak intensity = ", mean_peak_intensity)
    print(df)
    
