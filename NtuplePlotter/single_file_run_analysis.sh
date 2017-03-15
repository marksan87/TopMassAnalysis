#!/bin/bash
set -x
python top_mass_analysis.py -i /eos/uscms/store/user/msaunder/skims_13TeV/DoubleEG_Run2015D_Oct05.root -j ggNtuplizer_samples.json -o DoubleEG_Run2015D -n 10
