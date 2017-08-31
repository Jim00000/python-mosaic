# -*- coding:utf8 -*-
'''
    File name: mosaicplot.py
    Author   : Jim00000
    Created  : 8/31/2017
    Modified : 8/31/2017
'''

__author__    = "Jim00000"
__copyright__ = "Copyright 2017, the python-mosaic project"
__license__   = "GNU General Public License v3.0"
__version__   = "1.0.0"

import argparse
import sys
import os.path
import pickle
import numpy as np
# import matplotlib.pyplot as plt
import cv2

def load_vordig(filename):
    """Load Voronoi diagram

    Keyword arguments:
    filename -- pickle file containing seeds data

    Return:
    img      -- raw input image
    points_x -- collections of x position of seeds in one-dimension array
    points_y -- collections of y position of seeds in one-dimension array
    dic      -- a dictionary contaning cell points -> pixel data

    Exceptions:
    FileNotFoundError -- if argument 'filename' file does not exist 
    """
    # Check existence of files
    if os.path.isfile(filename) is False:
        raise FileNotFoundError('File \'%s\' does not exist' %filename )

    # Load seeds data
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        
    points_x = data['x']
    points_y = data['y']
    img = data['img']
    dic = data['dict']

    return img, points_x, points_y, dic

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

def plot_mosaic_edge(img, points_x, points_y, dic, rgb = [0, 0, 0]):
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
            is_not_edge = ( (y - 1,x) in pix_dic and  (y,x - 1) in pix_dic and (y + 1,x) in pix_dic and (y,x + 1) in pix_dic )

            # Check edge    
            if is_not_edge is False:
                output_img[y,x,:] = np.array(rgb)
    
    return output_img

def main(argv):
    """The entry for this program.

    Keyword arguments:
    argv -- arguments from terminal
    """
    # Arguments parsing
    parser = argparse.ArgumentParser(description='mosaic polt program')
    parser.add_argument("-input", "--input-vordig-file", default='vordig.pickle', type=str, help="input voronoi diagram pickle file (default : vordig.pickle) ")
    parser.add_argument("-o", "--output-file", default='output.jpg', type=str, help="output image file (default : output.jpg) ")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-pc", "--plot-centroidal", default=False, action="store_true", help="Use centroidal point as the color of the cell")
    group.add_argument("-pa", "--plot-average", default=False, action="store_true", help="Use average color of the cell as the color of all pixels inside the cell")
    parser.add_argument("-pme", "--plot-mosaic-edge", default=False, action="store_true", help="Plot edge for all cells")
    parser.add_argument("-rgb", type=int, nargs=3, default=[0, 0, 0],help="rgb for edge (default : [0, 0, 0])")
    args = parser.parse_args()

    # [DEBUG] Show arguments
    print(args)

    # Arguments
    vor_dig_data = args.input_vordig_file
    output_filename = args.output_file
    is_average_plot = args.plot_average
    is_centroidal_plot = args.plot_centroidal
    is_plot_mosaic_edge = args.plot_mosaic_edge
    rgb = args.rgb

    # If no one plot method is selected
    if (is_average_plot or is_centroidal_plot) is False:
        print('Warning: No drawing mehtod is selected, please choose one and restart this program')
        print('Type -h or --help for more information')
        sys.exit()

    # Load data from voronoi diagram 
    img, points_x, points_y, dic = load_vordig(vor_dig_data)

    # Plot pixel
    if is_average_plot is True:
        img = average_plot(img, points_x, points_y, dic)
    elif is_centroidal_plot is True:
        img = centroidal_plot(img, points_x, points_y, dic)
    else:
        print('Warning: No drawing mehtod is selected, please choose one and restart this program')
        print('Type -h or --help for more information')
        sys.exit()

    # Plot mosaic edge
    if is_plot_mosaic_edge is True:
        img = plot_mosaic_edge(img, points_x, points_y, dic, rgb = rgb)

    # Output image
    save_img(img, filename = output_filename)

    # Show done message
    print('Done!')

if __name__ == "__main__":
    """main function """
    main(sys.argv)