#!/bin/bash

#echo `NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/$1 root://cmsxrootd.fnal.gov///store/user/troy2012/ntuples_13TeV/$2`

############
### Data ###
############

if [ "$1" == "sts" ]; then
./skim /uscms_data/d1/msaunder/skims2017/mc_WWTo2L2Nu/mc_WWTo2L2Nu_0.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_WWTo2L2Nu/job_Summer16_WWTo2L2Nu_0.root 


elif [ "$1" == "sttwat" ]; then
./skim /uscms_data/d1/msaunder/skims2017/mc_ST_tW_antitop/mc_ST_tW_antitop_0.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_ST_tW_antitop/job_Summer16_ST_tW_antitop_0.root 


elif [ "$1" == "sttwt" ]; then
./skim /uscms_data/d1/msaunder/skims2017/mc_ST_tW_top/mc_ST_tW_top_0.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_ST_tW_top/job_Summer16_ST_tW_top_0.root 

else
 echo "Invalid argument"
fi
