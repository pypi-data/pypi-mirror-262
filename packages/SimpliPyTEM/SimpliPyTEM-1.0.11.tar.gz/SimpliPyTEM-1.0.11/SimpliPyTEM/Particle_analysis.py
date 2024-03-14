import math

import imutils
from imutils import contours
from moviepy.editor import ImageSequenceClip
from skimage import measure
import cv2 as cv
import numpy as np 
import pandas as pd 
from SimpliPyTEM.Micrograph_class import Micrograph
from SimpliPyTEM.MicroVideo_class import MicroVideo
import time
import concurrent.futures
from functools import partial
"""
MAIN FUNCTIONS
"""


def Threshold(image, threshold, brightfield=True):
    """
    Threshold the image to a particular value, such that below that value goes to black and above that value goes to white.

    Parameters
    ----------
        image:numpy array
            The image to be thresholded

        threshold: int
            The threshold value

    returns
    -------
        thresh:numpy array
            The thresholded image

    """

    imG = cv.GaussianBlur(image, (5, 5), 0)
    # croppedThresh[croppedThresh<90] = 0
    # croppedThresh[croppedThresh>90]=255
    ret, thresh = cv.threshold(imG, threshold, 255, cv.THRESH_BINARY)
    thresh = cv.erode(thresh, None, iterations=1)
    thresh = cv.dilate(thresh, None, iterations=1)
    thresh = thresh.astype("uint8")
    if brightfield == True:
        thresh = cv.bitwise_not(thresh)
    return thresh  # ,res


'''def Find_contours(
    thresh,
    minsize=200,
    complex_coords=False,
    maxsize=100000,
    remove_edges=True,
    labelled=False,
):
    """
    Finds the contours (or edges) of the particles in the image

    In doing so, this also filters the particles by minimum and maximum size (in number of pixels total area) and removes any particles which are on the edge of the image.

    Parameters
    ----------

        thresh:numpy array
            The thresholded image, can be produced with threshold(). Can also use a pre-labelled image (labelled=True)

        minsize:int
            The minimum area (in pixels) for a particle to be considered a particle

        minsize:int
            The maximum area (in pixels) for a particle to be considered a particle

        complex_coords:bool
            Whether to use cv.CHAIN_APPROX_SIMPLE or cv.CHAIN_APPROX_NONE in the contours. Complex_coords = False (off, chain_approx_simple) simplifies the bounding coordinates leading to less total coordinates, this is faster to process. Full coordinates (complex_coords=True) allows more detailed measurements across the particle, however will take longer.

        labelled: bool
            If you want to use a labelled image (rather than thresholded) set to true. Labelled image should have the pixels lablled a specific number for each particle
    Returns
    -------
        contours_im:list
            This is a list of arrays with coordinates which bound each particle selected in the image. This is used in downstream processing.

        mask:numpy array
            Binary image showing the particles selected in white and the background in black.

    """

    if labelled != True:
        cnts, hier = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in cnts:
            cv.drawContours(thresh, [cnt], 0, 255, -1)
        labels = measure.label(thresh, background=0)
    else:
        labels = thresh
    
    mask = np.zeros(thresh.shape, dtype="uint8")

    for label in np.unique(labels):
        label_mask = np.zeros(thresh.shape, dtype="uint8")
        label_mask[labels == label] = 255
        
        num_pixels = cv.countNonZero(label_mask)
    
        if not any([num_pixels < minsize,num_pixels > maxsize]):
            # print(coords)
            mask = cv.add(mask, label_mask)
            
    # Get the coordinates, this step chooses which types of coordinates are used.
    if complex_coords:
        contours_im = cv.findContours(
            mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE
        )
    else:
        contours_im = cv.findContours(
            mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )

    contours_im = imutils.grab_contours(contours_im)
    
    try:
        contours_im = contours.sort_contours(contours_im)[0]
    except ValueError:
        print(
            "Theres a ValueError! This is commonly because no particles are selected in the video.  Try raising the threshold value, or changing the minimum/maximum particle sizes"
        )

    
    #This bit filters particles on the edge of the image
    if remove_edges==True:
        contours_im_filtered=[]
        edge_threshold=5

        for contour in contours_im:
            is_touching_edge = False
            for point in contour:
                x, y = point[0]  # Extract x and y coordinates
                # Check if the point is within the edge_threshold distance from the image boundary
                if x < edge_threshold or x >= (thresh.shape[1] - edge_threshold) or \
                y < edge_threshold or y >= (thresh.shape[0] - edge_threshold):
                    is_touching_edge = True
                    break  # No need to check other points in this contour
            if not is_touching_edge:
                contours_im_filtered.append(contour)

        mask = np.zeros(thresh.shape, dtype=np.uint8)

        # Draw filled contours on the mask
        cv.drawContours(mask, contours_im_filtered, -1, (255), thickness=cv.FILLED)
    return contours_im_filtered, mask
'''

def Collect_particle_data(contours_im, pixel_size, multimeasure=False):
    """
    This collects a number of data sets from the contours_im outputted by the find_contours function. Complex measurement of particle size can be done with multimeasure (it measures the distance across each particle at multiple points and then includes max, min, mean and std of these measurements)

    Data collected for each particle in this function:
        Area - The area of the particle in the image
        Centroid - The center point coordinate of the particle (x, y)
        Aspect ratio - ratio between minimum and maximum length of particle
        Circularity - The area of the particle divided by the area of a circle that completely bounds the particle, giving a value for how circular it is (or how much of a circle it fills)
        width - The width of the smallest possible rectangle that could fully contain the particle
        Height - The height of the smallest possible rectangle that could fully contain the particle
        radius - The radius of the smallest possible circle that could fully contain the particle.
        Major-Minor Ratio  - the ratio between width and height

        Multimeasure specific:

            Max-diameter
            Min-diameter
            Mean-diameter
            Stddev-diameter
            Number of measurements  - the number of measurements across the particle to give the above diameter values.

        particle_data = { 'Area':area_particle, 'Centroid':centroid_particle,
                     'Aspect_ratio':aspect_ratio_particle, 'Perimeter':perimeter_particle, 'Circularity':circularity_particle,
                     'Width':width_particle, 'Height':height_particle, 'Radius':radius_particle, 'Major-Minor Ratio':MajorMinorRatio}

    Parameters
    ----------

        contours_im:list
            As generated from find_contours()
        pixel_size:float
            Pixel size in the image, the same unit is used in the output data so not important here but worth keeping an eye on.
        multimeasure:bool
            Whether to measure the distance across the particle many times, this can give an idea of the variation in shape and a better measure of diameter, but also  significantly increases runtime.

    Returns
    -------
        particle_data:dict
            A dictionary containing the data collected (with keys describing what the data is)
    """
    num_particle = len(contours_im)
    # print(num_particle)

    # this parameter computes the maximum length of a particle i.e. maximum distance between two point of a contour
    # max_length_particle = np.zeros([num_particle, 1], dtype=float)
    # this parameter computes the areas of  particles
    # area_particle = np.zeros([num_particle, 1], dtype=float)
    area_particle = []
    # this parameter computes the center of the mass of  particles
    centroid_x_particle = []
    centroid_y_particle = []
    centroid_particle = []
    # this parameter computes the ratio between maximum and minimum length of a particle
    aspect_ratio_particle = []
    # this parameter computes the perimeter of particles
    perimeter_particle = []
    # this parameter computes the perimeter of particles
    # circularity_particle = np.zeros([num_particle, 1], dtype=float)
    circularity_particle = []
    # width_particle =np.zeros([num_particle, 1], dtype = float)
    # height_particle = np.zeros([num_particle, 1], dtype = float)
    width_particle = []
    height_particle = []
    radius_particle = []
    # meanradius_particle=np.zeros([num_particle, 1],dtype = float)
    MajorMinorRatio = []

    if multimeasure:
        maxlength = []
        minlength = []
        meanlength = []
        stddev_length = []
        measurements = []
    for i, c in enumerate(contours_im):
        # print(i,c)
        moment_contour = cv.moments(c)
        centroid_x = moment_contour["m10"] / moment_contour["m00"]
        centroid_y = moment_contour["m01"] / moment_contour["m00"]
        centroid_x_particle.append(centroid_x)
        centroid_y_particle.append(centroid_y)
        centroid_particle.append((centroid_x, centroid_y))
        area = cv.contourArea(c) * pixel_size**2
        area_particle.append(area)
        # meanradius_particle = area__particle[i, 0]

        perimeter_particle.append(cv.arcLength(c, True) * pixel_size)
        min_rectangle = cv.minAreaRect(c)
        # print(min_rectangle)
        # circularity_particle =
        width_height = min_rectangle[1]
        # print(width, height)
        # width_particle[i, 0]= width*pixel_size
        # height_particle[i, 0] = height*pixel_size
        height = max(width_height)
        width = min(width_height)
        width_particle.append(width * pixel_size)
        height_particle.append(height * pixel_size)
        MajMinRat = height / width
        MajorMinorRatio.append(MajMinRat)
        ((cx, cy), radius) = cv.minEnclosingCircle(c)
        radius_particle.append(radius * pixel_size)
        circularity_particle.append(area / (np.pi * radius * radius * pixel_size**2))
        box = cv.boxPoints(min_rectangle)
        box = np.int0(box)

        if multimeasure:
            dists, coords = multiMeasure_particle(c, (centroid_x, centroid_y))
            maxlength.append(max(dists) * pixel_size)
            minlength.append(min(dists) * pixel_size)
            meanlength.append(np.mean(dists) * pixel_size)
            stddev_length.append(np.std(dists) * pixel_size)
            measurements.append(len(dists))

    particle_data = {
        "Area": area_particle,
        "Centroid": centroid_particle,
        "Centroid_x": centroid_x_particle,
        "Centroid_y": centroid_y_particle,
        "Perimeter": perimeter_particle,
        "Circularity": circularity_particle,
        "Width": width_particle,
        "Height": height_particle,
        "Radius": radius_particle,
        "Major-Minor Ratio": MajorMinorRatio,
    }
    if multimeasure:
        particle_data["Min diameter"] = minlength
        particle_data["Max diameter"] = maxlength
        particle_data["Mean diameter"] = meanlength
        particle_data["Stddev diameter"] = stddev_length
        particle_data["Measurements"] = measurements
    # print(particle_data)
    return particle_data


# particle_data=  Collect_particle_data(contours_im, 0.112)
# print(particle_data['Height'])
# print(np.mean(particle_data['Height']))

"""
PLOT RADIUS DATA
"""


# print(np.array(widths))
# widths_list = [x for i in widths for x in i]
def Flatten_list(l):
    """
    Simple function to make a single list from a list of lists, useful for combining data from different frames

    Parameters
    ----------

        l: list of list of lists
            These can be created if from the particle_analysis_video function or if you do particle analysis of multiple frames, the data from these can be combined with this function.
    Returns
    -------
        single list of values
    """
    return [x for i in l for x in i]


def Convert_to_single_dict(l, combine_data=False):
    """
    Take a list of dictionaries and convert to a single dictionary. This can keep data per image or combine the data from each image, as per requirements

    Parameters
    ----------

        l: list
            List of dictionaries containing particle data for each image

        combine_data:bool
            Do you want the data from each frame separated or together? True for together
    """
    # make an new empty dictionary
    alldata_dict = {}

    # Get the keys of the dictionaries

    keys = list(l[0].keys())

    # Create empty options for each key value
    for key in l[0].keys():
        alldata_dict[key] = []

    # Append the data from each dataset into the new dictionary
    for dset in l:
        for key in dset:
            alldata_dict[key].append(dset[key])

    alldata_dict["Image number"] = []
    for x in range(len(l)):
        alldata_dict["Image number"].append(([x for i in range(len(l[x][key]))]))
    if combine_data:
        for key in alldata_dict.keys():
            alldata_dict[key] = Flatten_list(alldata_dict[key])

    return alldata_dict


def Sidebyside(Video1, Video2):
    """
    Stitches two videos together side by side - (good for comparing masks and originals)

    Parameters
    ----------
        Video1:numpy array
            Lefthand video
        Video2:numpy array
            Righthand video
    Returns
    -------
        sidebyside: numpy array
            Single videos where the two videos play side by side
    """
    # Videos need to be the same shape. Add video as numpy stack (Z,Y,X )
    print(Video1.shape)
    z1, y1, x1 = Video1.shape
    z2, y2, x2 = Video2.shape
    sidebyside = np.zeros((max(z1, z2), max(y1, y2), x1 + x2), dtype="uint8")

    # this was put here to invert the masked video, DO this BEFORE calling function.
    # masksinv=cv.bitwise_not(np.array(masks))
    sidebyside[:, :, :x1] = Video1

    sidebyside[:, :, x1:] = Video2[:, :, :]
    # plt.imshow(sidebyside[0], cmap='magma')
    # plt.show()
    return sidebyside


def Particle_analysis(image, threshold, minsize, pixel_size, multimeasure=False):
    """
    Do the thresholding, contours finding and data collection all in one to collect data from the particles  in an image

    Parameters
    ----------
        image:numpy array
            The image to analyse
        threshold:int
            The threshold pixel value
        minsize:int
            minimum area of particles
        pixel_size:float
            Pixel size in the image, normally in nanometers but this unit is kept in the resulting data so it doesnt matter.
        Multimeasure:bool
            Whether to measure the distance across the particle many times, this can give an idea of the variation in shape and a better measure of diameter, but also  significantly increases runtime.

    Returns
    -------
        mask:numpy array
            A binary image showing the particles selected in white.

        particle_data:dict
            A dictionary containing the data collected (with keys describing what the data is)
    """

    thresh = Threshold(image, threshold)
    contours_im, mask = Find_contours(thresh, minsize)
    particle_data = Collect_particle_data(contours_im, pixel_size, multimeasure)
    return mask, particle_data


def Particle_analysis_video(video, threshold, minsize, pixel_size, multimeasure=False):
    """
    Runs the particle analysis for every frame in a video and creates a dictionary with a list of lists (data from each frame) as the value.

    Parameters
    ----------
        video:numpy array
            The video to analyse
        threshold:int
            The threshold pixel value
        minsize:int
            minimum area of particles
        pixel_size:float
            Pixel size in the image, normally in nanometers but this unit is kept in the resulting data so it doesnt matter.
        Multimeasure:bool
            Whether to measure the distance across the particle many times, this can give an idea of the variation in shape and a better measure of diameter, but also  significantly increases runtime.

    Returns
    -------
        mask:numpy array
            A binary video showing the particles selected in white.

        particle_data:dict
            A dictionary containing the data collected (with keys describing what the data is)
    """
    masks = []

    # video_data ={'Max_length':[], 'Area':[], 'Centroid':[],
    #                 'Aspect_ratio':[], 'Perimeter':[], 'Circularity':[],
    #                 'Width':[], 'Height':[], 'Radius':[], 'Major-Minor Ratio':[]}

    # if multimeasure:
    #    video_data['Min diameter'] = []
    #    video_data['Max diameter'] = []
    #    video_data['Mean diameter'] = []
    #    video_data['Stddev diameter']=[]
    #    video_data['Measurements']=[]
    # print(particle_data)
    video_data = {}

    i = 0

    for frame in video:
        mask, data = Particle_analysis(
            frame, threshold, minsize, pixel_size, multimeasure
        )
        masks.append(mask)

        if i == 0:
            for key in data.keys():
                video_data[key] = []
            i = 1

        for key in data:
            video_data[key].append(data[key])

    masks = np.array(masks)
    return masks, video_data


def multiMeasure_particle(particle_contours, centroid):
    """
    Measures the diameter of the particle at multiple points around the particle by seeing if the angle between any two points on the perimeter and the center of the particle is 180 +/- 1 degree.

    Parameters
    ----------
        particle_contours: list
            A list of the coordinates bounding the particle (each list within contours_im)

        centroid: array
            The central coordinate of the particle.

    returns
    -------
        distances: list
            A list  of the diameters measured
        coordinates
            The pairs of coordinates measured (point1, center point, point2)
    """
    distances = []
    coords = []
    c = centroid
    count = 0
    # print(c)
    # print(contours_im[0])
    for P1 in particle_contours:
        # print(P1[0])
        for P2 in particle_contours:
            # print(P1[0][0],P1[0][1],P2[0][1],c[0],P2[0][1] )
            # print('P1: ', P1)
            # print('P2: ', P2)
            # print('c: ', c)
            ba = P1[0] - c
            bc = P2[0] - c

            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.degrees(np.arccos(cosine_angle))

            if 179 < angle < 181:
                # print(angle)
                count += 1
                # d = np.linalg.norm(P1[0], P2[0])
                d = math.hypot(P1[0][0] - P2[0][0], P1[0][1] - P2[0][1])
                coords.append((P1[0], c, P2[0]))
                distances.append(d)
    return distances, coords




def Find_contours(
    thresh,
    minsize=200,
    complex_coords=False,
    maxsize=100000,
    remove_edges=True,
    labelled=False,
    threads=5
):


    #this part is filling in the particles
    if labelled != True:
        cnts, hier = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in cnts:
            cv.drawContours(thresh, [cnt], 0, 255, -1)
        labels = measure.label(thresh, background=0)
    else:
        labels = thresh

    
    
    #Filter each particle by size. This step uses multiple threads to speed it up.
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        partial_process_label = partial(process_label, maxsize=maxsize, minsize=minsize, shape=thresh.shape, labels=labels)
        label_masks = list(executor.map(partial_process_label, np.unique(labels)))

    # Add each of the label masks to a single file
    mask = np.zeros(thresh.shape, dtype="uint8")
    for label_mask in label_masks:
        if label_mask is not None:
            mask = cv.add(mask, label_mask)

    # Get the coordinates, this step chooses which types of coordinate systems are used.
    if complex_coords:
        contours_im = cv.findContours(
            mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE
        )
    else:
        contours_im = cv.findContours(
            mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )

    
    contours_im = imutils.grab_contours(contours_im)
    try:
        contours_im = contours.sort_contours(contours_im)[0]
    except ValueError:
        print(
            "Theres a ValueError! This is commonly because no particles are selected in the video.  Try raising the threshold value, or changing the minimum/maximum particle sizes"
        )

    #This bit filters particles on the edge of the image
    if remove_edges==True:
        contours_im_filtered=[]
        edge_threshold=5

        for contour in contours_im:
            is_touching_edge = False
            for point in contour:
                x, y = point[0]  # Extract x and y coordinates
                # Check if the point is within the edge_threshold distance from the image boundary
                if x < edge_threshold or x >= (thresh.shape[1] - edge_threshold) or \
                y < edge_threshold or y >= (thresh.shape[0] - edge_threshold):
                    is_touching_edge = True
                    break  # No need to check other points in this contour
            if not is_touching_edge:
                contours_im_filtered.append(contour)

        mask = np.zeros(thresh.shape, dtype=np.uint8)

        # Draw filled contours on the mask
        cv.drawContours(mask, contours_im_filtered, -1, (255), thickness=cv.FILLED)
    
    return contours_im_filtered, mask

def process_label(label, maxsize, minsize, shape,labels):
        #print(label)
        label_mask = np.zeros(shape, dtype="uint8")
        label_mask[labels == label] = 255
        num_pixels = cv.countNonZero(label_mask)
        if not any([num_pixels < minsize,num_pixels > maxsize]):
            return(label_mask)

