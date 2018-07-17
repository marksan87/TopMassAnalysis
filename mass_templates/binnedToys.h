#ifndef TOYS_H
#define TOYS_H

#include <TTree.h>
#include <vector>
vector< vector<float> > createToys(TTree* t, char* obsName, float cut, int ntoys = 100, int nbins = 100, float min = 25.0, float max = 225.0);

#endif
