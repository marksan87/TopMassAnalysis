from ROOT import *
import argparse
import sys
from array import array

def main():
    usage = 'usage %prog [options]'

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="input file (.txt)")
    args = parser.parse_args()

    etaMin = []
    etaMax = []
    ptMin = []
    ptMax = []
    eff = []
    statErr = []
    with open(args.file, 'r') as f:
	for line in f:
	    data = line.split()
	    etaMin.append(float(data[0]))
	    etaMax.append(float(data[1]))
	    ptMin.append(float(data[2]))
	    ptMax.append(float(data[3]))
	    eff.append(float(data[4]))
	    statErr.append(float(data[5]))
  
    xbins = []
    ybins = []

    xbins.append(etaMin[0])
    for eta in etaMax:
	if not eta in xbins:
	    xbins.append(eta)

    #print "xbins ", xbins

    ybins.append(ptMin[0])
    for pt in ptMax:
	if not pt in ybins:
	    ybins.append(pt)

    #print "ybins ", ybins    

    h = TH2F("SF", "Scale Factors", len(xbins)-1, array('f',xbins), len(ybins)-1, array('f', ybins))
 
    for bin in xrange(0, (len(ybins)-1)*(len(xbins)-1)):
	h.SetBinContent(h.FindBin(etaMin[bin]+0.001, ptMin[bin]+0.001), eff[bin])
	h.SetBinError(h.FindBin(etaMin[bin]+0.001, ptMin[bin]+0.001), statErr[bin])
	#h.SetBinContent(h.FindBin(etaMin[bin], ptMin[bin]), eff[bin])
    
    fname = args.file
    fname = fname[:fname.find('.')] + '.root'
    f = TFile.Open(fname, "recreate")
    h.Write()
    f.Close()


#    for a in xrange(0, (len(xbins)-1) * (len(ybins)-1)):
#	h.SetBinVa
    
#    for i in xrange(0, len(etaMin)):
#	print etaMin[i], etaMax[i], ptMin[i], ptMax[i], eff[i], statErr[i]

if __name__ == "__main__":
    sys.exit(main())
