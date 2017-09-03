# -*- coding:utf8 -*-
'''
    File name: voronoi.py
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
import time
import os.path
import pickle
import numpy as np
import matplotlib.pyplot as plt
import cv2
from external.progress.bar import FillingSquaresBar
from scipy.spatial import Voronoi, voronoi_plot_2d
from cppvoronoi.voronoi import cpp_voronoi_diagram

def generate_voronoi_diagram(width, height, point_x, point_y, iteration = 3):
    """Implement of Lloyd’s algorithm.
    We use this algorithm to get centroidal Voronoi diagrams.
    For more information, please refer to Simple Adaptive Mosaic Effects paper.

    Keyword arguments:
    width     -- width of input image
    height    -- height of input image
    point_x   -- collections of x position of seeds in one-dimension array
    point_y   -- collections of y position of seeds in one-dimension array
    iteration -- iteration (default : 3)

    Return:
    dic -- a dictionary contaning cell points -> pixel data 
    """

    bar = FillingSquaresBar('Processing', max=iteration * 3)
    
    for i in range(iteration):
        dic = initialize_dic(point_x.size)
        bar.next()
        # voronoi_diagram(width, height, point_x, point_y, dic)
        dic = cpp_voronoi_diagram(width, height, point_x, point_y, dic)
        bar.next()
        update_positions(dic, point_x, point_y)
        bar.next()

    
    bar.finish()
    return dic

def initialize_dic(size):
    """Initialize a dictionary containing every pixel belonging to which points 
    That is, every key in the dictionary has the pixel list belonging to the point (or cell)
    We use points to represent cells

    Keyword arguments:
    size -- seed points size

    Return:
    dic -- a dictionary contaning cell points -> pixel data 
    """
    dic = {}
    for i in range(size):
        # We push data pair (-1, -1) into dic for every point
        # It will be removed while processing something
        dic[i] = np.array([[-1], [-1]])
    return dic

def update_positions(dic, point_x, point_y):
    """Update every points position by averaging all the positions of pixels in the region 
    dominated by this point(or cell). 
    That is, new point position = average(positions of pixels belongs to this points).

    Keyword arguments:
    dic     -- a dictionary contaning cell points -> pixel data
    point_x -- collections of x position of seeds in one-dimension array
    point_y -- collections of y position of seeds in one-dimension array
    """
    for i in range(point_x.size):
        # Get all the pixels belongs to the cell and remove first dummy data pair (-1, -1)
        data = dic[i][:,1:]
        # Avoid that cells contain nothing but still process
        if(data.size > 0):
            new_px = round(np.average(data[0]))
            new_py = round(np.average(data[1]))
            point_x[i] = new_px
            point_y[i] = new_py

def voronoi_diagram(width, height, point_x, point_y, dic):
    """Compute voronoi diagram.
    For each piexl, calculate distance between this pixel and all points
    And put the pixel inside the dictionary whose key is the point that has the minimal distance

    Keyword arguments:
    width   -- width of input image
    height  -- height of input image
    point_x -- collections of x position of seeds in one-dimension array
    point_y -- collections of y position of seeds in one-dimension array
    dic     -- a dictionary contaning cell points -> pixel data
    """
    # For each pixel
    for y in range(height):
        for x in range(width):
            # Compute difference (position of cell - position of pixel)
            diff = np.array([point_x - x,point_y - y])
            # Calculate Euclidean distance
            dist = np.linalg.norm(diff, axis=0)
            # Find the smallest index inside the numpy array.
            # That is, the index stands for the cell (or point)
            index = np.argmin(dist)
            # Make new data pair
            coord = np.array([[x],[y]])
            # Put the new data pair inside the dictionary with its key is the point
            dic[index] = np.hstack((dic[index],coord))