# -*- coding:utf8 -*-
'''
    File name: plot.py
    Author   : Jim00000
    Created  : 12.22.2017
'''

__author__    = "Jim00000"
__copyright__ = "Copyright 2017, the python-mosaic project"
__license__   = "GNU General Public License v3.0"
__version__   = "1.0.0"

import numpy as np
import cv2

def save_img(img, filename='output.jpg'):
    """Save image

    Keyword arguments:
    img      -- the image 
    filename -- file name that will be saved
    """
    # Convert to BGR format
    output_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # Save image
    cv2.imwrite(filename, output_img)

def average_plot(img, points_x, points_y, dic):
    """ Draw pixel in input image using following method.
    Take the cell and compute average rgb values for every pixel

    Keyword arguments:
    img      -- input image
    points_x -- collections of x position of seeds in one-dimension array
    points_y -- collections of y position of seeds in one-dimension array
    dic      -- a dictionary contaning cell points -> pixel data

    Return:
    output_img -- image that has been colored
    """
    # Create an image buffer 
    output_img = np.full(img.size, 255).reshape(img.shape).astype(np.uint8)

    # For every cell
    for i in range(points_x.size):
        x = int(round(points_x[i]))
        y = int(round(points_y[i]))
        data = dic[i][:,1:]
        # Retrieve rbg value of raw image
        r = int(img[y,x,0])
        g = int(img[y,x,1])
        b = int(img[y,x,2])

        # For every pixel in the cell
        for j in range(data[0].size):
            tx = data[0][j]
            ty = data[1][j]
            r += img[ty,tx,0]
            g += img[ty,tx,1]
            b += img[ty,tx,2]

        # Compute average rgb value    
        r /= (data[0].size + 1)
        g /= (data[0].size + 1)
        b /= (data[0].size + 1)
        
        # Copy rbg value to centroidal point
        output_img[y, x, :] = np.array([r, g, b])
        # Copy rbg value to every pixel
        for j in range(data[0].size):
            tx = data[0][j]
            ty = data[1][j]
            output_img[ty, tx, :] = np.array([r, g, b])
        
    return output_img

def centroidal_plot(img, points_x, points_y, dic):
    """ Draw pixel in input image using following method.
    Take rgb values of centroidal point and fill to other pixels inside the cell

    Keyword arguments:
    img      -- input image
    points_x -- collections of x position of seeds in one-dimension array
    points_y -- collections of y position of seeds in one-dimension array
    dic      -- a dictionary contaning cell points -> pixel data

    Return:
    output_img -- image that has been colored
    """
    # Create an image buffer 
    output_img = np.full(img.size, 255).reshape(img.shape).astype(np.uint8)

    # For every cell
    for i in range(points_x.size):
        x = int(round(points_x[i]))
        y = int(round(points_y[i]))
        data = dic[i][:,1:]
        r = int(img[y,x,0])
        g = int(img[y,x,1])
        b = int(img[y,x,2])

        # Copy rbg of the centroidal point to output image
        output_img[y,x,:] = img[y,x,:]
        
        # Copy rbg to other pixels inside the cell
        for j in range(data[0].size):
            tx = data[0][j]
            ty = data[1][j]
            output_img[ty, tx, :] = img[y,x,:]
        
    return output_img

def plot_mosaic_edge(img, points_x, points_y, dic, rgb = [0, 0, 0], bold_edge = False):
    """Plot edges of every cell

    Keyword arguments:
    img      -- input image
    points_x -- collections of x position of seeds in one-dimension array
    points_y -- collections of y position of seeds in one-dimension array
    dic      -- a dictionary contaning cell points -> pixel data
    rgb      -- color of edges (default : rgb(0, 0, 0) black )

    Return:
    output_img -- image that has been colored edges
    """
    # Clone image
    output_img = np.copy(img)

    # For every cell
    for i in range(points_x.size):
        data = dic[i][:,1:]
        pix_dic = {}
        
        # Put pixels which belongs to a cell into dic
        for j in range(data[0].size):
            x = data[0][j]
            y = data[1][j]
            pix_dic[(y, x)] = True

        # For every pixel, check whether neighbor pixels exist
        # Plot the edge if the candidate pixel has neighbor pixels (In my way,
        # check upper pixel, lower pixel, left pixel and right pixel) 
        # being close to the candidate pixel
        for j in range(data[0].size): 
            x = data[0][j]
            y = data[1][j]
            if bold_edge is True:
                is_not_edge = ( 
                    (y - 1,x) in pix_dic and  
                    (y,x - 1) in pix_dic and 
                    (y + 1,x) in pix_dic and 
                    (y,x + 1) in pix_dic 
                    )
            else:
                is_not_edge = (
                    (y + 1,x) in pix_dic and 
                    (y,x + 1) in pix_dic 
                    )

            # Check edge    
            if is_not_edge is False:
                output_img[y,x,:] = np.array(rgb)
    
    return output_img

def adjust_gamma(img, gamma=1.0):
    """gamma adjustment

    Keyword arguments:
    img     -- input image
    gamma   -- the gamma value

    Return:
    output_img -- image that has been adjusted

    References:
    See also https://www.pyimagesearch.com/2015/10/05/opencv-gamma-correction/
    """
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
 
    # apply gamma correction using the lookup table
    return cv2.LUT(img, table)