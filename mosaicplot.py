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
from plot.plot import save_img, average_plot, centroidal_plot, plot_mosaic_edge, adjust_gamma

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
    group = parser.add_argument_group(title='mosaic edge options')
    group.add_argument("-pme", "--plot-mosaic-edge", default=False, action="store_true", help="Plot edge for all cells")
    group.add_argument("--bold-edge", default=False, action="store_true", help="Plot edge with bold line style")
    group.add_argument("-rgb", type=int, nargs=3, default=[0, 0, 0], help="Set rgb for edge (default : [0, 0, 0])")
    group.add_argument("--enable-gamma-correction", default=False, action="store_true", help="Enable gamma correction to adjust image")
    group.add_argument("-gamma", type=float, default=1.0, help="Set gamma value (default : 1.0)")
    args = parser.parse_args()

    # [DEBUG] Show arguments
    print(args)

    # Arguments
    vor_dig_data = args.input_vordig_file
    output_filename = args.output_file
    is_average_plot = args.plot_average
    is_centroidal_plot = args.plot_centroidal
    is_plot_mosaic_edge = args.plot_mosaic_edge
    is_bold_edge = args.bold_edge
    is_enable_gamma_correction = args.enable_gamma_correction
    gamma = args.gamma
    rgb = args.rgb

    # If no one plot method is selected
    if (is_average_plot or is_centroidal_plot) is False:
        print('Warning: No drawing mehtod is selected, please choose one and restart this program')
        print('Type -h or --help for more information')
        sys.exit()

    # Load data from voronoi diagram 
    img, points_x, points_y, dic = load_vordig(vor_dig_data)

    # Gamma adjustment
    if is_enable_gamma_correction is True:
        img = adjust_gamma(img, gamma)

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
        img = plot_mosaic_edge(img, points_x, points_y, dic, rgb = rgb, bold_edge = is_bold_edge)

    # Output image
    save_img(img, filename = output_filename)

    # Show done message
    print('Done!')

if __name__ == "__main__":
    """main function """
    main(sys.argv)