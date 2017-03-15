#!/bin/bash
set -x
rm pileup_wrap.cxx pileup_swig.o PUReweight.o _pileup.so
swig -c++ -python pileup.i
g++ -O2 -c -fPIC -o PUReweight.o -I`root-config --incdir` -std=c++11 PUReweight.cpp
g++ -O2 -c -fPIC -o pileup_swig.o -I/usr/include/python2.6 -I`root-config --incdir` -std=c++11 pileup_wrap.cxx
g++ -shared -o _pileup.so `root-config --libs` PUReweight.o pileup_swig.o
       
