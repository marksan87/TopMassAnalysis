from ROOT import *
import argparse
import sys
from array import array

def main():
    usage = 'usage %prog [options]'
    
    #parser = argparse.ArgumentParser()
    #parser.add_argument("file", help="input file (.txt)")
    #args = parser.parse_args()
    
    mu8_files = ['IsoMu8_271036-274093.txt', 'IsoMu8_274094-275000.txt', 'IsoMu8_275001-275783.txt', 'IsoMu8_275784-276500.txt', 'IsoMu8_276501-276811.txt']
    
    mu23_files = ['IsoMu23_271036-274093.txt', 'IsoMu23_274094-275000.txt', 'IsoMu23_275001-275783.txt', 'IsoMu23_275784-276500.txt', 'IsoMu23_276501-276811.txt']


    
    etaMin = []
    etaMax = []
    ptMin = []
    ptMax = []
    eff = []
    errUp = []
    errDn = []
    effList = []

    for i, inF in enumerate(mu23_files):
	if i == 0:
	    with open(inF, 'r') as f:
		for i, line in enumerate(f):
		    if i == 0: continue

		    data = line.split()
		    etaMin.append(float(data[0]))
		    etaMax.append(float(data[1]))
		    ptMin.append(float(data[2]))
		    ptMax.append(float(data[3]))
		    eff.append(float(data[4]))
		    errUp.append(float(data[5]))
		    errDn.append(float(data[6]))
		effList.append(eff)
	else:
	    eff = []
	    with open(inF, 'r') as f:
		for i, line in enumerate(f):
		    if i == 0: continue

		    data = line.split()
		    eff.append(float(data[4]))
		effList.append(eff)

    xbins = []
    ybins = []

    xbins.append(etaMin[0])
    for eta in etaMax:
	if not eta in xbins:
	    xbins.append(eta)

   # print "xbins ", xbins

    ybins.append(ptMin[0])
    for pt in ptMax:
	if not pt in ybins:
	    ybins.append(pt)

   # print "ybins ", ybins    
    h = TH2F("SF", "Scale Factors", len(xbins)-1, array('f',xbins), len(ybins)-1, array('f', ybins))
 
    for bin in xrange(0, (len(ybins)-1)*(len(xbins)-1)):
	binN = h.FindBin(etaMin[bin]+0.001, ptMin[bin]+0.001)
	h.SetBinContent(binN, ((effList[0])[bin] + (effList[1])[bin] + (effList[2])[bin] + (effList[3])[bin] + (effList[4])[bin]) / 5.0)
    
    fname = "Mu23_SF.root"
    #fname = fname[:fname.find('.')] + '.root'
    f = TFile.Open(fname, "recreate")
    h.Write()
    f.Close()


#    for a in xrange(0, (len(xbins)-1) * (len(ybins)-1)):
#	h.SetBinVa
    
#    for i in xrange(0, len(etaMin)):
#	print etaMin[i], etaMax[i], ptMin[i], ptMax[i], eff[i], statErr[i]

if __name__ == "__main__":
    sys.exit(main())
