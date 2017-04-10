from ROOT import *
import argparse
import sys
from array import array

def main():
    usage = 'usage %prog [options]'

    parser = argparse.ArgumentParser()
    parser.add_argument("plot", help="plot file")
    args = parser.parse_args()

    f = TFile.Open("NtuplePlotter/plots_mt1785/plots/plotter.root")
    #f = TFile.Open("NtuplePlotter/plots2017/plots/plotter.root")
    d = f.Get(args.plot)

    data = d.Get(args.plot)
    mc = d.Get("totalmc")
    chi2 = data.Chi2Test(mc, "UW CHI2/NDF")
    print "chi2 from",args.plot, "=", chi2


if __name__ == "__main__":
    sys.exit(main())
