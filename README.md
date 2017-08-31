# Introduction

This project implementing approach which comes from an IEEE paper, **Simple Adaptive Mosaic Effects**, makes users be able to add mosaic effect to images  

# Prerequisite

Make sure  **python3** has been installed and that will be used in this project, **python2 is not working**

And install necessary libraries

```
$ pip3 install --user -r requirements.txt
```

# Usage

First step, generate seeds from raw image

```
$ python3 seedgen.py <image-file>
```

You will get a pickle file (default : seed.pickle) containing seeds data when this process completes

Also, you can  tune parameters like minimal area in pixels and error rate, or output the seed distribution to check. Type `--help` to see more information

# Reference

- [Simple Adaptive Mosaic Effects](http://ieeexplore.ieee.org/document/1599119/)

# License

GNU General Public License v3.0