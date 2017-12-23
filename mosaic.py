# -*- coding:utf8 -*-
'''
    File name: mosaic.py
    Author   : Jim00000 <good0121good@gmail.com>
    Created  : 12.23.2017
'''

__author__ = "Jim00000"
__copyright__ = "Copyright 2017, the python-mosaic project"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"

import os.path
import sys
import argparse
import cv2
from quad.quad import Quad
from voronoi.voronoi import generate_voronoi_diagram
from plot.plot import save_img, average_plot, centroidal_plot, plot_mosaic_edge, adjust_gamma


def main(argv):
    # Arguments parsing
    parser = argparse.ArgumentParser(
        description='A tool to add mosaic effect to images')
    parser.add_argument("filename", help="Input image file", type=str)
    parser.add_argument("-o", "--output-file", default="output.jpg",
                        type=str, help="The output file for mosaic effect images")
    group = parser.add_argument_group(title='mosaic seed generator')
    group.add_argument("--error-rate", default=0.5,
                       type=float, help="error rate (default:0.5)")
    group.add_argument("--min-area", default=64, type=int,
                       help="minimal pixels for each block (default:64)")
    group.add_argument("--enable-gaussian-blur", default=False,
                       action="store_true", help="Apply Gaussian blur")
    group = parser.add_argument_group(title='mosaic voronoi graph generator')
    group.add_argument("-t", "--iter", default=5, type=int,
                       help="Iteration time for Lloyd’s algorithm (default:5)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-pc", "--plot-centroidal", default=False,
                       action="store_true", help="Use centroidal point as the color of the cell (default:False)")
    group.add_argument("-pa", "--plot-average", default=True, action="store_true",
                       help="Use average color of the cell as the color of all pixels inside the cell (default:True)")
    group = parser.add_argument_group(title='mosaic edge options')
    group.add_argument("-pme", "--plot-mosaic-edge", default=False,
                       action="store_true", help="Plot edge for all cells")
    group.add_argument("--bold-edge", default=False,
                       action="store_true", help="Plot edge with bold line style")
    group.add_argument("-rgb", type=int, nargs=3,
                       default=[0, 0, 0], help="Set rgb for edge (default : [0, 0, 0])")
    group.add_argument("--enable-gamma-correction", default=False,
                       action="store_true", help="Enable gamma correction to adjust image")
    group.add_argument("-gamma", type=float, default=1.0,
                       help="Set gamma value (default : 1.0)")
    args = parser.parse_args()

    # [DEBUG] Show arguments
    print(args)

    # Assign arguments
    imgfile = args.filename
    output_file = args.output_file
    error_rate = args.error_rate
    min_area = args.min_area
    is_gaussian_blur = args.enable_gaussian_blur
    iteration = args.iter
    is_average_plot = args.plot_average
    is_centroidal_plot = args.plot_centroidal
    is_plot_mosaic_edge = args.plot_mosaic_edge
    is_bold_edge = args.bold_edge
    is_enable_gamma_correction = args.enable_gamma_correction
    gamma = args.gamma
    rgb = args.rgb

    # Check the existence of the image file
    if os.path.isfile(imgfile) is False:
        raise FileNotFoundError('File \'%s\' does not exist' % imgfile)

    # If no one plot method is selected
    if (is_average_plot or is_centroidal_plot) is False:
        print('Warning: No drawing mehtod is selected, please choose one and restart this program')
        print('Type -h or --help for more information')
        sys.exit()

    # Load image and store as array (convert to RGB)
    img = cv2.imread(imgfile)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Apply gaussian blur
    if is_gaussian_blur is True:
        img = cv2.GaussianBlur(img, (5, 5), 0)

    # Compute regional quadrature tree
    quad_root = Quad(img, min_area=min_area,
                     error_rate=error_rate, is_root=True)

    # Generate seeds
    points_x, points_y = quad_root.generate_seeds()

    # Generate voronoi diagram
    height = img.shape[0]
    width = img.shape[1]
    dic = generate_voronoi_diagram(
        width, height, points_x, points_y, iteration=iteration)

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
        img = plot_mosaic_edge(img, points_x, points_y,
                               dic, rgb=rgb, bold_edge=is_bold_edge)

    # Output image
    save_img(img, filename=output_file)

    # Show done message
    print('Done!')


if __name__ == "__main__":
    """main function """
    main(sys.argv)
