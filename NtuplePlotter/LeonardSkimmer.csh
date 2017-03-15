#!/bin/bash
cd ..

#echo `NtuplePlotter/skim_test root://cmseos.fnal.gov//store/user/msaunder/skims_13TeV/$1 root://cmsxrootd.fnal.gov///store/user/troy2012/ntuples_13TeV/$2`

############
### Data ###
############

if [ "$1" == "d1" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims_2016/full/DoubleEG_Run2016B_PRv2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_DoubleEG_Run2016B_PRv2.root 

############
###  MC  ###
############

elif [ $1 == "M" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims2017/mc_TTZ_withHLT.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/mc_TTZ_withHLT.root

elif [ $1 == "mm" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims2017/mc_WWTo2L2Nu.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/mc_WWTo2L2Nu.root
#NtuplePlotter/skim /uscms_data/d1/msaunder/skims2017/mc_Fan_TTZToLLNuNu.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/mc_Fan_TTZToLLNuNu.root 

#NtuplePlotter/skim /uscms_data/d1/msaunder/topMassAnalysis/CMSSW_8_0_24_patch1/src/ttgamma_13TeV/NtuplePlotter/WJetsToLNu_test.root root://eoscms.cern.ch//store/user/pbarria/ggntuples/mc/V08_00_24_00/output/job_spring16_WJetsToLNu_aMCatNLO_miniAOD.root

elif [ $1 == "m1" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_TTWJetsToLNu.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_spring16_TTWJetsToLNu_aMCatNLO.root

elif [ $1 == "m2" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_TTZToLLNuNu.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_spring16_TTZToLLNuNu.root

elif [ $1 == "m3" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_WWTo2L2Nu.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_spring16_WWTo2L2Nu.root

elif [ $1 == "m4" ]; then
NtuplePlotter/skim_2016_full /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_TT.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/job_spring16_TT_powheg_ext3.root

elif [ $1 == "m5" ]; then
NtuplePlotter/skim_2016_full /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_ST_s.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/ST_s.root

elif [ $1 == "m6" ]; then
NtuplePlotter/skim_2016_full /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_ST_tW_antitop.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/ST_tW_antitop.root

elif [ $1 == "m7" ]; then
NtuplePlotter/skim_2016_full /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_ST_t_antitop.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/ST_t_antitop.root

elif [ $1 == "m8" ]; then
NtuplePlotter/skim_2016_full /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_ST_t_top.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/ST_t_top.root

elif [ $1 == "m9" ]; then
NtuplePlotter/skim_2016_full /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_WJetsToLNu_aMCatNLO.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/job_spring16_WJetsToLNu_aMCatNLO.root

elif [ $1 == "m10" ]; then
NtuplePlotter/skim_2016_full /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_DYJetsToLL_m50_aMCatNLO.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/job_spring16_DYJetsToLL_m50_aMCatNLO.root

elif [ $1 == "a" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims2017/mc_WJetsToLNu/mc_WJetsToLNu_0.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_WJetsToLNu/job_Summer16_WJetsToLNu_0.root

elif [ $1 == "b" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims2017/mc_WJetsToLNu/mc_WJetsToLNu_1.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_WJetsToLNu/job_Summer16_WJetsToLNu_1.root


elif [ $1 == "c" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims2017/mc_WJetsToLNu/mc_WJetsToLNu_2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_WJetsToLNu/job_Summer16_WJetsToLNu_2.root


elif [ $1 == "d" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims2017/mc_WJetsToLNu/mc_WJetsToLNu_3.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_WJetsToLNu/job_Summer16_WJetsToLNu_3.root


elif [ $1 == "e" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims2017/mc_TT/mc_TT_4.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_TT/job_Summer16_TT_4.root

elif [ $1 == "f" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims2017/mc_TT/mc_TT_5.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_TT/job_Summer16_TT_5.root

elif [ $1 == "g" ]; then
NtuplePlotter/skim /uscms_data/d1/msaunder/skims2017/mc_TT/mc_TT_6.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_TT/job_Summer16_TT_6.root

else
 echo "Invalid argument"
fi
