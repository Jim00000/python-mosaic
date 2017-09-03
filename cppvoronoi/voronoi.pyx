from libcpp.map cimport map
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from cpython cimport array
import numpy as np

cdef extern from "Voronoi.h" namespace "cpp":
    cdef cppclass Voronoi:
        void diagram(int, int, vector[int], vector[int], map[int,vector[pair[int,int]]]*);

def cpp_voronoi_diagram(width, height, point_x, point_y, dic):
    cdef map[int,vector[pair[int,int]]] *m = new map[int,vector[pair[int,int]]]();
    cdef Voronoi *vor = new Voronoi();
    vor.diagram(width, height, point_x, point_y, m);
    dic = m[0]

    del vor;
    del m;

    for i in range(point_x.size):
        xy = np.array(dic[i]).T.reshape(2, len(dic[i]))
        dic[i] = xy

    return dic