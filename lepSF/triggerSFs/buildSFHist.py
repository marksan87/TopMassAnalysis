from ROOT import *
import argparse
import sys
from array import array

def main():
    usage = 'usage %prog [options]'

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="input file (.txt)")
    args = parser.parse_args()

    ptl1Min = []
    ptl1Max = []
    ptl2Min = []
    ptl2Max = []
    eff = []
    error = []
    with open(args.file, 'r') as f:
	for i, line in enumerate(f):
	    if i == 0: continue  # Skip header line

	    data = line.split()
	    ptl1Min.append(float(data[0]))
	    ptl1Max.append(float(data[1]))
	    ptl2Min.append(float(data[2]))
	    ptl2Max.append(float(data[3]))
	    eff.append(float(data[4]))
	    error.append(float(data[5]))
  
    xbins = []
    ybins = []

    xbins.append(ptl1Min[0])
    for pt in ptl1Max:
	if not pt in xbins:
	    xbins.append(pt)

   # print "xbins ", xbins

    ybins.append(ptl2Min[0])
    for pt in ptl2Max:
	if not pt in ybins:
	    ybins.append(pt)

   # print "ybins ", ybins    
    h = TH2F("SF", "Scale Factors", len(xbins)-1, array('f',xbins), len(ybins)-1, array('f', ybins))
 
    for bin in xrange(0, (len(ybins)-1)*(len(xbins)-1)):
	b = h.FindBin(ptl1Min[bin]+0.001, ptl2Min[bin]+0.001)
	h.SetBinContent(b, eff[bin])
	h.SetBinError(b, error[bin])
    
    fname = args.file
    fname = fname[:fname.find('.')] + '.root'
    f = TFile.Open(fname, "recreate")
    h.Write()
    f.Close()



if __name__ == "__main__":
    sys.exit(main())
