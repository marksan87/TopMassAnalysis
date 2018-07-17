#!/usr/bin/env python
from ROOT import *
from numpy import mean,std
from pprint import pprint
from datetime import datetime
from argparse import ArgumentParser
import os
import sys
gSystem.CompileMacro("toys.C", "gOck")
gSystem.Load("toys_C")
masses = ['1665', '1695', '1715', '1725', '1735', '1755', '1785']
obsTitle = {"ptll":"p_{T}(ll)", "ptpos":"p_{T}(l^{+})", "Epos":"E(l^{+})", "ptp_ptm":"p_{T}(l^{+}) + p_{T}(l^{-})", "Ep_Em":"E(l^{+}) + E(l^{-})", "Mll":"M(ll)"}


def main():
    parser = ArgumentParser()
    parser.add_argument("-i", "--inDir", default="ttrees/tt",help="path to directory of ttree files")
    parser.add_argument("--obs", "-d", default="ptll", help="kinematic distribution to analyze")
    parser.add_argument("--cut", "-c", default = 180, help="upper limit to cut on (or -1 for no cut)", type=float)
    parser.add_argument("-r", dest="level", default="rec", help="rec,gen")
    parser.add_argument("-m", "--mass", default = "1725", help="top mass file")
    parser.add_argument("-t", "--ntoys", default = 10, help="number of toys to generate", type=int)
    parser.add_argument("-o", "--outDir", default="", help="directory to output files to")
    args = parser.parse_args()

    if args.inDir[-1] == '/':
        args.inDir = args.inDir[:-1]
    
    if args.outDir == "":
        args.outDir = "Ctoys_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    elif args.outDir[-1] == '/':
        args.outDir = args.outDir[:-1]

    if args.level not in ["rec","gen"]:
        print "Invalid reconstruction level. Choose one of the following: rec,gen"
        sys.exit()

    if args.obs not in obsTitle.keys():
        print "Invalid observable. Choose one of the following:", obsTitle.keys()
        sys.exit()

    if args.mass not in masses:
        print "Invalid mass. Choose from %s" % masses
        sys.exit()

    if args.ntoys < 0:
        print "Number of toys must be > 0. Defaulting to 10"
        args.ntoys = 10

    print "\nOpening file %s/mc_TT-mt%s.root.." % (args.inDir, args.mass),
    f = TFile.Open("%s/mc_TT-mt%s.root" % (args.inDir, args.mass), "read")
    t = f.Get("goodEvents")
    print "done."

    obsName = "%s_%s" % (args.level, args.obs)

    moments = createToys(t, obsName, args.cut, args.ntoys)

    _w  = moments[0]
    _m1 = moments[1]
    _m2 = moments[2]
    weights = []
    m1 = []
    m2 = []
    for w in _w: weights.append(w) 
    for m in _m1: m1.append(m)
    for m in _m2: m2.append(m)
    print "\nmt = %.1f results:" % (float(args.mass)/10.)
    print "Moment 1 toys: %f  +- %f" % (mean(m1),std(m1))
    print "Moment 2 toys: %f +- %f" %  (mean(m2),std(m2))
    print "Weights:"
    print weights
    os.system("mkdir -p %s" % args.outDir)
    with open ("%s/%s_mt%s.txt" % (args.outDir, obsName, args.mass), "w") as f:
        f.write("%s\n%s\n%s" % (m1,m2,weights))
    print "\nMoments saved in %s/%s_mt%s.txt" % (args.outDir, obsName, args.mass)

if __name__ == "__main__":
    sys.exit(main())
