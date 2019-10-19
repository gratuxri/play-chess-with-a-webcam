# see:
# https://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_image_histogram_calcHist.php
# https://giusedroid.blogspot.com/2015/04/using-python-and-k-means-in-hsv-color.html

import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

def do_cluster(hsv_image, K, channels):
    # gets height, width and the number of channes from the image shape
    h,w,c = hsv_image.shape
    # prepares data for clustering by reshaping the image matrix into a (h*w) x c matrix of pixels
    cluster_data = hsv_image.reshape( (h*w,c) )
    # grabs the initial time
    t0 = t.time()
    # performs clustering
    codebook, distortion = kmeans(np.array(cluster_data[:,0:channels], dtype=np.float), K)
    # takes the final time
    t1 = t.time()
    print ("Clusterization took %0.5f seconds" % (t1-t0))


    # calculates the total amount of pixels
    tot_pixels = h*w
    # generates clusters
    data, dist = vq(cluster_data[:,0:channels], codebook)
    # calculates the number of elements for each cluster
    weights = [len(data[data == i]) for i in range(0,K)]

    # creates a 4 column matrix in which the first element is the weight and the other three
    # represent the h, s and v values for each cluster
    color_rank = np.column_stack((weights, codebook))
    # sorts by cluster weight
    color_rank = color_rank[np.argsort(color_rank[:,0])]

    # creates a new blank image
    new_image =  np.array([0,0,255], dtype=np.uint8) * np.ones( (500, 500, 3), dtype=np.uint8)
    img_height = new_image.shape[0]
    img_width  = new_image.shape[1]

    # for each cluster
    for i,c in enumerate(color_rank[::-1]):

        # gets the weight of the cluster
        weight = c[0]

        # calculates the height and width of the bins
        height = int(weight/float(tot_pixels) *img_height )
        width = img_width/len(color_rank)

        # calculates the position of the bin
        x_pos = i*width



        # defines a color so that if less than three channels have been used
        # for clustering, the color has average saturation and luminosity value
        color = np.array( [0,128,200], dtype=np.uint8)

        # substitutes the known HSV components in the default color
        for j in range(len(c[1:])):
            color[j] = c[j+1]

        # draws the bin to the image
        new_image[ img_height-height:img_height, x_pos:x_pos+width] = [color[0], color[1], color[2]]

    # returns the cluster representation
    return new_image

def plotChannel(hsv,channel,col,rows,plotNum,title):
  cImg=hsv[:,:,channel]
  plt.subplot(rows,col,plotNum)
  plt.hist(np.ndarray.flatten(cImg),bins=256)
  plt.title(title)

def main(argv):
    default_file = '../testMedia/chessBoard001.jpg'
    filename = argv[0] if len(argv) > 0 else default_file
    image = cv2.imread(filename)
    cv2.imshow('chessboard',image)
    # refresh
    cv2.waitKey(10)
    hsv=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    plt.figure(figsize=(10,8))
    plt.suptitle('HSV Histogramm', fontsize=16)
    plotChannel(hsv,0,1,4,2,'Hue')
    plt.subplots_adjust(hspace=.5)
    plotChannel(hsv,1,1,4,3,'Saturation')
    plotChannel(hsv,2,1,4,4,'Luminosity Value')
    fig=plt.figure(1)
    fig.canvas.set_window_title('Histogramm for %s' % (filename))
    plt.show()
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])
