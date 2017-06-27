#!/bin/bash
set -x
python top_mass_analysis.py --inDir /uscms_data/d1/msaunder/skims2017 -p ../Pileup/pileup_processed_lumimasked.root -j mt1735.json -o plots_mt1735 -n 17
source /cvmfs/cms.cern.ch/cmsset_default.csh

pushd plots_mt1735
hadd -f mc_DYJetsToLL.root mc_DYJetsToLL_*
hadd -f mc_ST_s.root mc_ST_s_*
hadd -f mc_ST_tW_antitop.root mc_ST_tW_antitop_*
hadd -f mc_ST_tW_top.root mc_ST_tW_top_*
hadd -f mc_ST_t_antitop.root mc_ST_t_antitop_*
hadd -f mc_ST_t_top.root mc_ST_t_top_*
hadd -f mc_TT_mt1735.root mc_TT_mt1735_*
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
popd
python plotter.py -i plots_mt1735 -j mt1735.json -l 35862.0
