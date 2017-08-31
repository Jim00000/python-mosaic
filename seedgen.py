# -*- coding:utf8 -*-
'''
    File name: seedgen.py
    Author   : Jim00000
    Created  : 8/30/2017
    Modified : 8/31/2017
'''

__author__    = "Jim00000"
__copyright__ = "Copyright 2017, the python-mosaic project"
__license__   = "GNU General Public License v3.0"
__version__   = "1.0.0"

import pickle
import os.path
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import cv2
from quad.quad import Quad

def save_data(point_x, point_y, filename, img):
    """Dump the points into a file.

    Keyword arguments:
    point_x  -- one-dimension array stores seed points x
    point_y  -- one-dimension array stores seed points y
    filename -- file name that will be saved
    img      -- three-dimensions array represents rgb of an image
    """
    seed = {
        'x' : point_x,
        'y' : point_y,
        'img' : img
    }
    
    # Store seed
    with open(filename, 'wb') as f:
        pickle.dump(seed, f, pickle.HIGHEST_PROTOCOL)
        print("Seed data dumped as file \'%s\'" %filename )

def main(argv):
    """The entry for this program.

    Keyword arguments:
    argv -- arguments from terminal
    """
    # Arguments parsing
    parser = argparse.ArgumentParser(description='mosaic seeds generator')
    parser.add_argument("image", help="input image file", type=str)
    parser.add_argument("-o", "--output-seed", default='seed.pickle', type=str, help="output seeds pickle file")
    parser.add_argument("-od", "--output-dist", type=str, help="output seeds distribution image")
    parser.add_argument("-ocd", "--output-compsite-dist", type=str, help="output composite image of seeds distribution and input image")
    parser.add_argument("-e", "--error-rate", default=0.5, type=float, help="error rate (default:0.5)")
    parser.add_argument("-ma", "--min-area", default=64, type=int, help="minimal pixels for each block (default:64)")
    args = parser.parse_args()

    # [DEBUG] Show arguments
    print(args)

    # Assign arguments
    imgfile = args.image
    seed_filename = args.output_seed
    output_dist = args.output_dist
    output_compsite_dist = args.output_compsite_dist
    error_rate = args.error_rate
    min_area = args.min_area

    # Check the existence of the image file
    if os.path.isfile(imgfile) is False:
        raise FileNotFoundError('File \'%s\' does not exist' %imgfile )

    # Load image and store as array (convert to RGB)
    img = cv2.imread(imgfile)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Compute regional quadrature tree
    quad_root = Quad(img, min_area = min_area, error_rate = error_rate, is_root = True)

    # Generate seeds
    point_x, point_y = quad_root.generate_seeds()

    # Dump seeds data 
    save_data(point_x, point_y, seed_filename, img)

    # Output seeds distribution (if users set flags)
    if output_dist is not None:
        plt.plot(point_x, -point_y, 'o' , color='black', markersize=1)
        plt.axis('off')
        plt.savefig(output_dist, dpi=800)
        plt.clf()

    # Output composite image (if user set flags)
    if output_compsite_dist is not None:
        plt.plot(point_x, point_y, 'ro', markersize=1)
        plt.imshow(img)
        plt.axis('off')
        plt.savefig(output_compsite_dist, dpi=800)
        plt.clf()
    
    # Show Result
    seed_count = point_x.size
    print('Seed count : %d' %seed_count )

    # Show success message
    print('Done!')

if __name__ == "__main__":
    """main function """
    main(sys.argv)