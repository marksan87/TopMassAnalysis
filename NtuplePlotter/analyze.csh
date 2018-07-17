#!/bin/bash
set -x
python top_mass_analysis.py --inDir /uscms_data/d1/msaunder/skims2017 -p ../Pileup/pileupHistos.root -j allSamples.json -o plots2018 -n 19 --no-histos

#python top_mass_analysis.py --inDir /uscms_data/d1/msaunder/skims2017 -p ../Pileup/pileup_processed_lumimasked.root -j allSamples.json -o plots2018 -n 19 --no-histos
#python top_mass_analysis.py --inDir /uscms_data/d1/msaunder/skims2017 -p ../Pileup/pileup_Sep16ReReco.root -j ntuples2017.json -o plots2017 -n 17
#python combined_top_analysis.py --inDir /uscms_data/d1/msaunder/skimsCombined2017 -p ../Pileup/pileup_Sep16ReReco.root -j ntuples2017.json -o plots2017 -n 17
