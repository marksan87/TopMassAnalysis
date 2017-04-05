%module roccor 

%{
#define SWIG_FILE_WITH_INIT
#include "TRandom3.h" 
#include "TMath.h"
#include "TSystem.h"
#include "RoccoR.h"

%}

%include "typemaps.i"
%include "std_vector.i"
%include "std_string.i"
%include "cstring.i"
%include "cpointer.i"
%include "RoccoR.h"

