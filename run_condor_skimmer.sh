#!/bin/bash

job=$1


cd /uscms/home/msaunder/ggNtuples/CMSSW_7_4_16/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
cd /uscms/home/msaunder/ggNtuples/CMSSW_7_4_16/src/ttgamma_13TeV/

#outputDir="/uscms/home/msaunder/ggNtuples/CMSSW_7_4_16/src/ttgamma_13TeV/"
outputDir=${_CONDOR_SCRATCH_DIR}
inputfiles=("sync.root /uscms/home/msaunder/ggNtuples/CMSSW_7_4_16/src/ggAnalysis/ggNtuplizer/test/ggtree_sync.root")

echo "NtuplePlotter/makeSkim ${outputDir}${inputfiles[job]}"

#NtuplePlotter/makeSkim ${outputDir}${inputfiles[job]}
./makeSkim ${outputDir}${inputfiles[job]}

