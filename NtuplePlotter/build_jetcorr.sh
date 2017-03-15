#!/bin/bash
set -x
rm jetCorrection_wrap.cxx JECvariation.o EventTree_fPIC.o _jetCorrection.so
swig -c++ -python jetCorrection.i
g++ -O2 -c -fPIC -o JECvariation.o -I`root-config --incdir` -std=c++11 JECvariation.cpp
g++ -O2 -c -fPIC -o EventTree_fPIC.o -I`root-config --incdir` -std=c++11 EventTree.cpp
g++ -O2 -c -fPIC -o jetCorrection_swig.o -I/usr/include/python2.6 -I`root-config --incdir` -std=c++11 jetCorrection_wrap.cxx
g++ -shared -o _jetCorrection.so `root-config --libs` JECvariation.o jetCorrection_swig.o JetMETObjects/FactorizedJetCorrector.o JetMETObjects/JetCorrectorParameters.o JetMETObjects/SimpleJetCorrector.o JetMETObjects/JetCorrectionUncertainty.o JetMETObjects/SimpleJetCorrectionUncertainty.o EventTree_fPIC.o

