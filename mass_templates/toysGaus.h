#ifndef TOYS_H
#define TOYS_H

#include <TTree.h>
#include <vector>
vector< vector<float> > createToys(TTree* t, char* obsName, float cut, int ntoys = 100);

#endif
