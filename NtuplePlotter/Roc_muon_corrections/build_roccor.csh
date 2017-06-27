#!/bin/bash
set -x
rm roccor.o roccor_wrap.o roccor.py roccor_wrap.cxx _roccor.so
swig -c++ -python roccor.i
#../../swig-3.0.12/swig -c++ -python roccor.i
gcc -O2 -c -fPIC -o roccor.o -I`root-config --incdir` -std=c++14 RoccoR.cc
gcc -O2 -c -fPIC -o roccor_wrap.o -I/usr/include/python2.6 -I`root-config --incdir` -std=c++14 roccor_wrap.cxx
g++ -shared -o _roccor.so `root-config --libs` roccor.o roccor_wrap.o
