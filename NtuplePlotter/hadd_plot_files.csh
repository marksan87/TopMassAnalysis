#!/bin/csh
source /cvmfs/cms.cern.ch/cmsset_default.csh

cd plots2017
hadd -f mc_DYJetsToLL.root mc_DYJetsToLL_*
hadd -f mc_ST_s.root mc_ST_s_*
hadd -f mc_ST_tW_antitop.root mc_ST_tW_antitop_*
hadd -f mc_ST_tW_top.root mc_ST_tW_top_*
hadd -f mc_ST_t_antitop.root mc_ST_t_antitop_*
hadd -f mc_ST_t_top.root mc_ST_t_top_*
hadd -f mc_TT.root mc_TT_*
hadd -f mc_TTWJetsToLNu.root mc_TTWJetsToLNu_*
hadd -f mc_TTZToLLNuNu.root mc_TTZToLLNuNu_*
hadd -f mc_WJetsToLNu.root mc_WJetsToLNu_*
hadd -f mc_WWTo2L2Nu.root mc_WWTo2L2Nu_*
hadd -f mc_WZTo3LNu.root mc_WZTo3LNu_*
hadd -f mc_ZZTo2L2Nu.root mc_ZZTo2L2Nu_*
hadd -f MuEG_Run2016B.root MuEG_Run2016B_*
hadd -f MuEG_Run2016C.root MuEG_Run2016C_*
hadd -f MuEG_Run2016D.root MuEG_Run2016D_*
hadd -f MuEG_Run2016E.root MuEG_Run2016E_*
hadd -f MuEG_Run2016F.root MuEG_Run2016F_*
hadd -f MuEG_Run2016G.root MuEG_Run2016G_*
hadd -f MuEG_Run2016H.root MuEG_Run2016H_*
#hadd -f DoubleEG_Run2016B.root DoubleEG_Run2016B_*
#hadd -f DoubleEG_Run2016C.root DoubleEG_Run2016C_*
#hadd -f DoubleEG_Run2016D.root DoubleEG_Run2016D_*
#hadd -f DoubleEG_Run2016E.root DoubleEG_Run2016E_*
#hadd -f DoubleEG_Run2016F.root DoubleEG_Run2016F_*
#hadd -f DoubleEG_Run2016G.root DoubleEG_Run2016G_*
#hadd -f DoubleEG_Run2016H.root DoubleEG_Run2016H_*
#hadd -f DoubleMu_Run2016B.root DoubleMu_Run2016B_*
#hadd -f DoubleMu_Run2016C.root DoubleMu_Run2016C_*
#hadd -f DoubleMu_Run2016D.root DoubleMu_Run2016D_*
#hadd -f DoubleMu_Run2016E.root DoubleMu_Run2016E_*
#hadd -f DoubleMu_Run2016F.root DoubleMu_Run2016F_*
#hadd -f DoubleMu_Run2016G.root DoubleMu_Run2016G_*
#hadd -f DoubleMu_Run2016H.root DoubleMu_Run2016H_*

