# This function comes from : https://stackoverflow.com/questions/19122690/fast-peak-finding-and-centroiding-in-python/19137303
# it is used to find the centroid of the biggest spot detected on an image
import numpy as np
import scipy.ndimage

def centroide(Z):

    threshold   = Z.max()*0.8#/4
    
     
    #Set everything below the threshold to zero:
    Z_thresh = np.copy(Z)
    Z_thresh[Z_thresh<threshold] = 0
     
    #now find the objects
    labeled_image, number_of_objects = scipy.ndimage.label(Z_thresh)
     
    peak_slices = scipy.ndimage.find_objects(labeled_image)
     
    def centroid(data):
        h,w = np.shape(data)   
        x = np.arange(0,w)
        y = np.arange(0,h)
     
        X,Y = np.meshgrid(x,y)
     
        cx = np.sum(X*data)/np.sum(data)
        cy = np.sum(Y*data)/np.sum(data)
     
        return cx,cy
     
    centroids = []
    centroides=[]
    max_surface=0
    for peak_slice in peak_slices:
        dy,dx  = peak_slice
        x,y = dx.start, dy.start
        width  = (dx.stop - dx.start + 1)
        height = (dy.stop - dy.start + 1)
    
        cx,cy = centroid(Z_thresh[peak_slice])
        
        if width*height>max_surface: # Only keep the biggest one to ignore if there are "dead/hot pixel" above threshold :
            max_surface=width*height
            centroides=([x+cx,y+cy])
        centroids.append((x+cx,y+cy))

    return centroides
