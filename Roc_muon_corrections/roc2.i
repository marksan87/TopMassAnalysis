%module jetCorrection

%{
#include "TRandom3.h" 
#include "TMath.h"
#include "RoccoR.h"
#include "TSystem.h"

%}

%include "typemaps.i"
%include "std_vector.i"
%include "std_string.i"
%include "cstring.i"
%include "cpointer.i"

/*
namespace std {

        %template(IntVector) std::vector<int>;
        %template(FloatVector) std::vector<float>;
        %template(RCVector) std::vector<std::vector<RocOne> >;
        
};

*/
