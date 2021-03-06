#include <iostream>
#include <cmath>
#include <omp.h>
#include "Voronoi.h"

using namespace cpp;

typedef int key_t;
typedef std::vector<std::pair<int,int>> value_t;

inline double norm2(double dx, double dy) {
    return sqrt(pow(dx, 2) + pow(dy, 2));
}

inline double norm2(int dx, int dy) {
    return sqrt(pow(dx, 2) + pow(dy, 2));
}

void
Voronoi::diagram(
    int width,
    int height,
    std::vector<int> point_x,
    std::vector<int> point_y, 
    std::map<int,std::vector<std::pair<int,int>>> *dic
) 
{
    int sz = point_x.size();

    for(int i = 0; i < sz; i++) {
        ((*dic)[i]).push_back(std::make_pair(-1,-1));
    }

    #pragma omp parallel for schedule(dynamic)   
    for(int y = 0; y < height; y++) {
        for(int x = 0; x < width; x++) {
            
            // Calculate Euclidean distance and find its index
            double min = norm2(width, height);
            int minarg = -1;
            for(int i=0;i<sz;i++) {
                double dx = point_x[i] - x;
                double dy = point_y[i] - y;
                double dist = norm2(dx, dy);
                if(dist < min) {
                    min = dist;
                    minarg = i;
                }
            }

            // Push data
            #pragma omp critical
            if(minarg != -1) {
                ((*dic)[minarg]).push_back(std::make_pair(x, y));
            }

        }
    }

}
