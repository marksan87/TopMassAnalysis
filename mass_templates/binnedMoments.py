from ROOT import *
from array import array
MASSES = [166.5, 169.5, 171.5, 172.5, 173.5, 175.5, 178.5]

inDir = "ttrees/tt"


for m in MASSES:
    mstr = str(m).replace(".","")
    f = TFile.Open("%s/mc_TT-mt%s.root" % (inDir, mstr), "read")
    t = f.Get("goodEvents")
    t.Draw("rec_ptll >> h%s" % mstr, "rec_ptll >= 30 && rec_ptll <= 230")
    exec("h%s.SetDirectory(0)" % mstr)

