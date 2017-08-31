# -*- coding:utf8 -*-
'''
    File name: quad.py
    Author   : Jim00000
    Created  : 8/31/2017
    Modified : 8/31/2017
'''

__author__    = "Jim00000"
__copyright__ = "Copyright 2017, the python-mosaic project"
__license__   = "GNU General Public License v3.0"
__version__   = "1.0.0"

import queue
import math
import numpy as np

class Quad:
    
    def __init__(self, img, x = 0, y = 0, min_area = 64, error_rate = 0.5, is_root = False):
        """Quad constructor 

        Keyword arguments:
        img -- the input image
        x   -- the upper-left x position of this image
        y   -- the upper-left y position of this image
        """
        self.img = img
        self.height = img.shape[0]
        self.width = img.shape[1]
        self.x = x
        self.y = y
        self.min_area = min_area
        self.error_rate = error_rate
        self.is_root = is_root
        self.leaf = self.is_leaf() # Show that is this node a leaf
        self.children = None
        # If this node is root then generate the quadtree
        if is_root is True:
            self.leaves = self.generate_tree()

    def generate_tree(self):
        """Generate the quadtree 
        Note: it is legal to call only when the tree node is root
        """
        # Verify the caller is root
        if self.is_root is False:
            raise Exception('The caller is not a root')

        leaves = list()
        # Create a queue and push root 
        qu = queue.Queue()
        qu.put(self)
        
        # Pop all the elements out the queue in the same level and
        # put inside children with level - 1 if this node has children
        # until the queue is empty
        while qu.empty() is False:
            q_size = qu.qsize()
            # For all the elements in the same level
            for _ in range(q_size):
                child = qu.get()
                # If the node is a leaf then do nothing and appends it to the leaves list
                if child.leaf is False:
                    tl, tr, bl, br = child.__subdivide__()
                    qu.put(tl)
                    qu.put(tr)
                    qu.put(bl)
                    qu.put(br)
                else:
                    leaves.append(child)
        
        return leaves

    def __subdivide__(self):
        """Subdivide this quadrature tree and produce four child """
        # Compute width and height of the child region
        child_width = math.ceil(self.width / 2)
        child_height = math.ceil(self.height / 2)
        # Generate four sub-quadtree nodes
        top_left = Quad(self.img[:child_height,:child_width,:], x = self.x, y = self.y, min_area = self.min_area, error_rate = self.error_rate)
        top_right = Quad(self.img[:child_height,child_width:,:], x = self.x, y = self.y + child_width, min_area = self.min_area, error_rate = self.error_rate)
        bottom_left = Quad(self.img[child_height:,:child_width,:], x = self.x + child_height, y = self.y, min_area = self.min_area, error_rate = self.error_rate)
        bottom_right = Quad(self.img[child_height:,child_width:,:], x = self.x + child_height, y = self.y + child_width, min_area = self.min_area, error_rate = self.error_rate)
        # Mark all children
        self.children = [top_left, top_right, bottom_left, bottom_right]
        return top_left, top_right, bottom_left, bottom_right
    
    def is_leaf(self):
        """Check whether this node is a leaf """
        if self.height * self.width < self.min_area :
            return True
        else:
            if __error__(self.img) <= self.error_rate:
                return True
            else:
                return False

    def generate_seeds(self):
        """Generate seeds """
        point_x = np.zeros(len(self.leaves))
        point_y = np.zeros(len(self.leaves))

        for i in range(len(self.leaves)):
            block = self.leaves.pop()
            x = block.x
            y = block.y
            w = block.width
            h = block.height
            point_y[i] = x + w / 2
            point_x[i] = y + h / 2
        
        return point_x, point_y

def __error__(img):
    """Compute the error """
    avg_rgb = __average_rgb__(img)
    d2 = np.sum(np.power( (img - avg_rgb) / 255, 2), axis=2)
    err = d2.max(axis=1).max(axis=0).max()
    return err
    
def __average_rgb__(img):
    """Get average rgb value """
    r = np.average(img[:,:,0])
    g = np.average(img[:,:,1])
    b = np.average(img[:,:,2])
    return np.array([r,g,b])
