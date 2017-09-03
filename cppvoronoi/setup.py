from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        Extension(
            "voronoi",                 
            sources=["voronoi.pyx","Voronoi.cpp"], 
            language="c++",
            extra_compile_args=["-std=c++11", "-O3", "-msse"]            
        )
    )
)