#!/bin/csh
if ($#argv == 0) then
    echo "Must suuply an input directory!"
else
    cmsenv
    cd ..
    NtuplePlotter/skim $argv[1] $argv[2]
endif

