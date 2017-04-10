from ROOT import *
import argparse
import sys
from array import array

def main():
    usage = 'usage %prog [options]'

    parser = argparse.ArgumentParser()
    parser.add_argument("plot", help="plot file")
    args = parser.parse_args()
    
    fmain = TFile.Open("NtuplePlotter/plots2017/plots/plotter.root")
    dmain = fmain.Get(args.plot)

    f1665 = TFile.Open("NtuplePlotter/plots_mt1665/plots/plotter.root")
    d1665 = f1665.Get(args.plot)
    
    f1695 = TFile.Open("NtuplePlotter/plots_mt1695/plots/plotter.root")
    d1695 = f1695.Get(args.plot)

    f1715 = TFile.Open("NtuplePlotter/plots_mt1715/plots/plotter.root")
    d1715 = f1715.Get(args.plot)

    f1735 = TFile.Open("NtuplePlotter/plots_mt1735/plots/plotter.root")
    d1735 = f1735.Get(args.plot)
    
    f1755 = TFile.Open("NtuplePlotter/plots_mt1755/plots/plotter.root")
    d1755 = f1755.Get(args.plot)
    
    f1785 = TFile.Open("NtuplePlotter/plots_mt1785/plots/plotter.root")
    d1785 = f1785.Get(args.plot)

    mcmain = dmain.Get("totalmc")
    mc1665 = d1665.Get("totalmc")
    mc1695 = d1695.Get("totalmc")
    mc1715 = d1715.Get("totalmc")
    mc1735 = d1735.Get("totalmc")
    mc1755 = d1755.Get("totalmc")
    mc1785 = d1785.Get("totalmc")
    data = dmain.Get(args.plot)
    
    chi1665 = data.Chi2Test(mc1665, "UW CHI2")
    chi1695 = data.Chi2Test(mc1695, "UW CHI2")
    chi1715 = data.Chi2Test(mc1715, "UW CHI2")
    chi1735 = data.Chi2Test(mc1735, "UW CHI2")
    chi1755 = data.Chi2Test(mc1755, "UW CHI2")
    chi1785 = data.Chi2Test(mc1785, "UW CHI2")
    
#    chi1665 = mcmain.Chi2Test(mc1665, "WW CHI2")
#    chi1695 = mcmain.Chi2Test(mc1695, "WW CHI2")
#    chi1715 = mcmain.Chi2Test(mc1715, "WW CHI2")
#    chi1735 = mcmain.Chi2Test(mc1735, "WW CHI2")
#    chi1755 = mcmain.Chi2Test(mc1755, "WW CHI2")
#    chi1785 = mcmain.Chi2Test(mc1785, "WW CHI2")
    
#    chi1665 = mcmain.Chi2Test(mc1665, "WW CHI2/NDF")
#    chi1695 = mcmain.Chi2Test(mc1695, "WW CHI2/NDF")
#    chi1715 = mcmain.Chi2Test(mc1715, "WW CHI2/NDF")
#    chi1735 = mcmain.Chi2Test(mc1735, "WW CHI2/NDF")
#    chi1755 = mcmain.Chi2Test(mc1755, "WW CHI2/NDF")
#    chi1785 = mcmain.Chi2Test(mc1785, "WW CHI2/NDF")
#
    print "mt = 166.5: chi2 = ", chi1665
    print "mt = 169.5: chi2 = ", chi1695
    print "mt = 171.5: chi2 = ", chi1715
    print "mt = 173.5: chi2 = ", chi1735
    print "mt = 175.5: chi2 = ", chi1755
    print "mt = 178.5: chi2 = ", chi1785

#    f = TFile.Open("NtuplePlotter/plots_mt1785/plots/plotter.root")
#    #f = TFile.Open("NtuplePlotter/plots2017/plots/plotter.root")
#    d = f.Get(args.plot)
#
#    data = d.Get(args.plot)
#    mc = d.Get("totalmc")
#    chi2 = data.Chi2Test(mc, "UW CHI2/NDF")
#    print "chi2 from",args.plot, "=", chi2


if __name__ == "__main__":
    sys.exit(main())
