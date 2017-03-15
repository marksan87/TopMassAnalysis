#!/bin/csh
if ($#argv == 0) then
    echo "Must suuply an input directory!"

else
    cmsenv
    set numFiles = `eosls $argv[2] | grep 'ggtree*' | wc -l`
    echo "$numFiles"
    python skim_parallel.py $argv[1] $argv[2] $numFiles $argv[3]
endif

