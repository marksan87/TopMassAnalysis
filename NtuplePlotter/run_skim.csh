#!/bin/bash

############
### Data ###
############

if [ "$1" == "d1" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/DoubleEG_Run2016B_PRv2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_DoubleEG_Run2016B_PRv2.root 

elif [ "$1" == "d2" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/DoubleEG_Run2016C_PRv2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_DoubleEG_Run2016C_PRv2.root

elif [ "$1" == "d3" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/DoubleEG_Run2016D_PRv2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_DoubleEG_Run2016D_PRv2.root

elif [ "$1" == "d4" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/DoubleMuon_Run2016B_PRv2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_DoubleMu_Run2016B_PRv2.root

elif [ "$1" == "d5" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/DoubleMuon_Run2016C_PRv2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_DoubleMu_Run2016C_PRv2.root

elif [ "$1" == "d6" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/DoubleMuon_Run2016D_PRv2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_DoubleMu_Run2016D_PRv2.root

elif [ "$1" == "d7" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/MuonEG_Run2016B_PRv2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_MuEG_Run2016B_PRv2.root

elif [ "$1" == "d8" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/MuonEG_Run2016C_PRv2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_MuEG_Run2016C_PRv2.root

elif [ "$1" == "d9" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/MuonEG_Run2016D_PRv2.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_MuEG_Run2016D_PRv2.root

elif [ "$1" == "D" ]; then
./skim /uscms_data/d1/msaunder/skims2017/data_MuEG_Run2016F.root root://eoscms.cern.ch//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_24_00/job_MuEG_Run2016F_SepRereco1/ggtree_data_81.root root://eoscms.cern.ch//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_24_00/job_MuEG_Run2016F_SepRereco1/ggtree_data_82.root root://eoscms.cern.ch//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_24_00/job_MuEG_Run2016F_SepRereco1/ggtree_data_83.root
#/skim /uscms_data/d1/msaunder/skims2017/data_MuEG_Run2016F.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/data_MuEG_Run2016F_SepRereco1.root root://eoscms.cern.ch//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_24_00/job_MuEG_Run2016F_SepRereco1/ggtree_data_81.root

############
###  MC  ###
############

elif [ $1 == "stta0" ]; then
./skim /uscms_data/d1/msaunder/skims2017/mc_ST_t_antitop/mc_ST_t_antitop_0.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/job_Summer16_ST_t_antitop_0.root

elif [ $1 == "M" ]; then
./skim /uscms_data/d1/msaunder/skims2017/mc_TTZ_withHLT.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/mc_TTZ_withHLT.root

elif [ $1 == "mm" ]; then
./skim /uscms_data/d1/msaunder/skims2017/mc_WWTo2L2Nu.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/mc_WWTo2L2Nu.root
#/skim /uscms_data/d1/msaunder/skims2017/mc_Fan_TTZToLLNuNu.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2017/mc_Fan_TTZToLLNuNu.root 

#/skim /uscms_data/d1/msaunder/topMassAnalysis/CMSSW_8_0_24_patch1/src/ttgamma_13TeV//WJetsToLNu_test.root root://eoscms.cern.ch//store/user/pbarria/ggntuples/mc/V08_00_24_00/output/job_spring16_WJetsToLNu_aMCatNLO_miniAOD.root

elif [ $1 == "m1" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_TTWJetsToLNu.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_spring16_TTWJetsToLNu_aMCatNLO.root

elif [ $1 == "m2" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_TTZToLLNuNu.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_spring16_TTZToLLNuNu.root

elif [ $1 == "m3" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_WWTo2L2Nu.root root://cmseos.fnal.gov//store/user/msaunder/ntuples2016/job_spring16_WWTo2L2Nu.root

elif [ $1 == "m4" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_TT.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/job_spring16_TT_powheg_ext3.root

elif [ $1 == "m5" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_ST_s.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/ST_s.root

elif [ $1 == "m6" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_ST_tW_antitop.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/ST_tW_antitop.root

elif [ $1 == "m7" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_ST_t_antitop.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/ST_t_antitop.root

elif [ $1 == "m8" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_ST_t_top.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/ST_t_top.root

elif [ $1 == "m9" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_WJetsToLNu_aMCatNLO.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/job_spring16_WJetsToLNu_aMCatNLO.root

elif [ $1 == "m10" ]; then
./skim /uscms_data/d1/msaunder/skims_2016/full/mc_spring16_DYJetsToLL_m50_aMCatNLO.root root://cmseos.fnal.gov//store/user/troy2012/ntuples_2016/job_spring16_DYJetsToLL_m50_aMCatNLO.root


else
 echo "Invalid argument"
fi
