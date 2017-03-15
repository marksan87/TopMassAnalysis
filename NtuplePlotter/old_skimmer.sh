#!/bin/bash
cd ..

#echo `NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/$1 root://cmsxrootd.fnal.gov///store/user/troy2012/ntuples_13TeV/$2`

############
### Data ###
############

if [ $1 == "10" ] || [ $1 == "DoubleEG_Run2015C_Oct05" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/DoubleEG_Run2015C_Oct05.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_DoubleEG_Run2015C_Oct05_miniAOD.root

elif [ $1 == "11" ] || [ $1 == "DoubleEG_Run2015D_Oct05" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/DoubleEG_Run2015D_Oct05.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_DoubleEG_Run2015D_Oct05_miniAOD.root

elif [ $1 == "12" ] || [ $1 == "DoubleEG_Run2015D_PR_v4" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/DoubleEG_Run2015D_PR_v4.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_DoubleEG_Run2015D_PR_v4_miniAOD.root

############
###  MC  ###
############

elif [ $1 == "0" ] || [ $1 == "mc_spring15_DYJetsToLL_m50" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/mc_spring15_DYJetsToLL_m50.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_spring15_DYJetsToLL_m50_miniAOD.root

elif [ $1 == "1" ] || [ $1 == "mc_spring15_TT" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/mc_spring15_TT.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_spring15_TT_miniAOD.root

elif [ $1 == "2" ] || [ $1 == "mc_spring15_TTG" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/mc_spring15_TTG.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_spring15_TTG_miniAOD.root

elif [ $1 == "3" ] || [ $1 == "mc_spring15_TTWToLNu" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/mc_spring15_TTWToLNu.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_spring15_TTWToLNu_miniAOD.root

elif [ $1 == "4" ] || [ $1 == "mc_spring15_WJetsToLNu_aMCatNLO" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/mc_spring15_WJetsToLNu_aMCatNLO.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_spring15_WJetsToLNu_aMCatNLO_miniAOD.root


##############
# Single Top #
##############

elif [ $1 == "5" ] || [ $1 == "mc_spring15_ST_s" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/mc_spring15_ST_s.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_spring15_ST_s_miniAOD.root

elif [ $1 == "6" ] || [ $1 == "mc_spring15_ST_t_antitop_4f" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/mc_spring15_ST_t_antitop_4f.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_spring15_ST_t_antitop_4f_miniAOD.root

elif [ $1 == "7" ] || [ $1 == "mc_spring15_ST_t_top_4f" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/mc_spring15_ST_t_top_4f.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_spring15_ST_t_top_4f_miniAOD.root

elif [ $1 == "8" ] || [ $1 == "mc_spring15_ST_tW_antitop" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/mc_spring15_ST_tW_antitop.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_spring15_ST_tW_antitop_miniAOD.root

elif [ $1 == "9" ] || [ $1 == "mc_spring15_ST_tW_top" ]; then
NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/doubleE_full/mc_spring15_ST_tW_top.root root://cmsxrootd.fnal.gov//store/user/msaunder/ntuples_13TeV/V07_04_16_03/job_spring15_ST_tW_top_miniAOD.root


else
 echo "Invalid argument"
fi
