from ROOT import *
f = TFile.Open("SFs.root")
h = f.Get("Scale Factors")
print "(-0.81, 14.9) -> ", h.GetBinContent(h.FindBin(-0.81, 14.9))
