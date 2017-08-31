# -*- coding:utf8 -*-
'''
    File name: voronoigen.py
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
import matplotlib.pyplot as plt
from voronoi.voronoi import generate_voronoi_diagram
from scipy.spatial import Voronoi, voronoi_plot_2d

def load_seed(filename):
    """Load seeds data 

    Keyword arguments:
    filename -- pickle file containing seeds data

    Return:
    img     -- raw input image
    point_x -- collections of x position of seeds in one-dimension array
    point_y -- collections of y position of seeds in one-dimension array

    Exceptions:
    FileNotFoundError -- if argument 'filename' file does not exist 
    """
    # Check existence of files
    if os.path.isfile(filename) is False:
        raise FileNotFoundError('File \'%s\' does not exist' %filename )

    # Load seeds data
    with open(filename, 'rb') as f:
        seeds = pickle.load(f)
        
    point_x = seeds['x']
    point_y = seeds['y']
    img = seeds['img']

    return img, point_x, point_y

def save_data(img, points_x, points_y, dic, filename = "vordig.pickle"):
    """Dump dictionary, points_x, points_y, image into a pickle file.

    Keyword arguments:
    img      -- raw input image
    point_x  -- one-dimension array stores seed points x
    point_y  -- one-dimension array stores seed points y
    dic      -- a dictionary contaning cell points -> pixel data 
    filename -- file name that will be saved (default : 'vordig.pickle')
    """
    data = {
        'x' : points_x,
        'y' : points_y,
        'img' : img,
        'dict' : dic
    }
    
    # Store data
    with open(filename, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        print("Data dumped as file \'%s\'" %filename )


def preview_voronoi_diagram(points_x, points_y):
    """Preview Voronoi diagram

    Keyword arguments:
    points_x -- collections of x position of seeds in one-dimension array
    points_y -- collections of y position of seeds in one-dimension array
    """
    points_xy = np.vstack((points_x, -points_y)).T
    vor = Voronoi(points_xy)
    voronoi_plot_2d(vor, show_points = False, show_vertices = False)
    plt.axis('off')
    plt.savefig('preview.jpg', dpi=800)
    plt.clf()

def main(argv):
    """The entry for this program.

    Keyword arguments:
    argv -- arguments from terminal
    """
    # Arguments parsing
    seedfile = 'seed.pickle'

    # Load seeds data
    img, points_x, points_y = load_seed(seedfile)
    height = img.shape[0] 
    width = img.shape[1]

    # Generate voronoi diagram
    dic = generate_voronoi_diagram(width, height, points_x, points_y, iteration = 5)

    # Preview voronoi diagram
    # preview_voronoi_diagram(points_x, points_y)

    # Dump voronoi diagram data
    save_data(img, points_x, points_y, dic)

    # Print down message
    print('Done!')

if __name__ == "__main__":
    """main function """
    main(sys.argv)