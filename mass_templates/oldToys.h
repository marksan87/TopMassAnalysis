#ifndef TOYS_H
#define TOYS_H

#include <TTree.h>
#include <vector>
//vector<float> createToys(TTree* t, char* obsName, float cut, int npoints = 1000, int ntoys = 100);
vector< vector<float> > createToys(TTree* t, char* obsName, float cut, int npoints = 1000, int ntoys = 100);
//vector<float> loop(TTree* t, TRandom3* r, char* obsName, float cut);


#endif
