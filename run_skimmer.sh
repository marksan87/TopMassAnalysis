#!/bin/bash

job=$1

cd /uscms/home/msaunder/ggNtuples/CMSSW_7_4_16/src
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
cd /uscms/home/msaunder/ggNtuples/CMSSW_7_4_16/src/ttgamma_13TeV

#cd ${_CONDOR_SCRATCH_DIR}

outputDir="/uscms/home/msaunder/ggNtuples/CMSSW_7_4_16/src/ttgamma_13TeV/"

# The two arguments two the makeSkim script. The first is the output file. The second is the input file(s)
inputfiles=("sync.root /uscms/home/msaunder/ggNtuples/CMSSW_7_4_16/src/ggAnalysis/ggNtuplizer/test/ggtree_sync.root")

#echo "NtuplePlotter/makeSkim ${outputDir}${inputfiles[job]}"

NtuplePlotter/makeSkim ${outputDir}${inputfiles[job]}  
#./makeSkim ${outputDir}${inputfiles[job]}      
