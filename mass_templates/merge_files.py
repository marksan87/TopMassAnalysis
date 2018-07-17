#!/usr/bin/env python
from glob import glob
import os
from argparse import ArgumentParser



parser = ArgumentParser()
parser.add_argument("-i", dest="inDir", default = "Ctoys_2018*", help="Ctoys directory to glob for")
parser.add_argument("-m", dest="mt", default="1725", help="mass point")
parser.add_argument("-o", dest="outDir", default="Ctoys_merged", help="kinematic distribution to analyze")
args = parser.parse_args()




dirs = glob(args.inDir)
m1 = []
m2 = []
for d in dirs:
    with open("%s/rec_ptll_mt%s.txt" % (d, args.mt), "r") as f:
        for i,line in enumerate(f):
            exec("_m%d = %s" % (i+1,line))
            exec("m%d += _m%d" % (i+1,i+1))

os.system("mkdir -p %s" % args.outDir)
with open("%s/rec_ptll_mt%s.txt" %(args.outDir, args.mt), "w") as f:
    f.write("%s" % m1)
    f.write("\n")
    f.write("%s" % m2)
