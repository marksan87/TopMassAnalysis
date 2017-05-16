from ROOT import *
import argparse
import sys
from array import array

def CHI2(d, m):

    n=0
    ps=0
    mc_bins = m.GetNbinsX() #Mc bins
    data_bins = d.GetNbinsX() #Data bins
    chi2=0

    if mc_bins is not data_bins:
	print "Different number of bins in data and mc!"
	return

    
    while (n < mc_bins):
            
        O=d.GetBinContent(n)
        E=m.GetBinContent(n)
	if E == 0:
	    print "value in bin", n, "is 0!"
	    n+=1
	    continue
	
	#print "Bin ",n,"  mc:", E, "  data:",O
	print "Bin ",n," discrepancy: ", O-E 
	ps = ((O-E)**2.0)/((E)**2.0)
        chi2 += ps
        n += 1
        
    return chi2

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
   
    #mcmain.Sumw2()
    #mc1665.Sumw2()
    #mc1695.Sumw2()
    #mc1715.Sumw2()
    #mc1735.Sumw2()
    #mc1755.Sumw2()
    #mc1785.Sumw2()

    """
    chi1665 = CHI2(mcmain, mc1665)
    chi1695 = CHI2(mcmain, mc1695)
    chi1715 = CHI2(mcmain, mc1715)
    chi1735 = CHI2(mcmain, mc1735)
    chi1755 = CHI2(mcmain, mc1755)
    chi1785 = CHI2(mcmain, mc1785)
    """
    """
    chi1665 = CHI2(data, mc1665)
    chi1695 = CHI2(data, mc1695)
    chi1715 = CHI2(data, mc1715)
    chi1735 = CHI2(data, mc1735)
    chi1755 = CHI2(data, mc1755)
    chi1785 = CHI2(data, mc1785)
    """
    """ 
    chi1665 = data.Chi2Test(mc1665, "CHI2")
    chi1695 = data.Chi2Test(mc1695, "CHI2")
    chi1715 = data.Chi2Test(mc1715, "CHI2")
    chi1735 = data.Chi2Test(mc1735, "CHI2")
    chi1755 = data.Chi2Test(mc1755, "CHI2")
    chi1785 = data.Chi2Test(mc1785, "CHI2")
    """
    
    chi1665 = data.Chi2Test(mc1665, "UW  CHI2/NDF")
    chi1695 = data.Chi2Test(mc1695, "UW  CHI2/NDF")
    chi1715 = data.Chi2Test(mc1715, "UW  CHI2/NDF")
    chi1735 = data.Chi2Test(mc1735, "UW  CHI2/NDF")
    chi1755 = data.Chi2Test(mc1755, "UW  CHI2/NDF")
    chi1785 = data.Chi2Test(mc1785, "UW  CHI2/NDF")
     
     
     
#    chi1665 = mcmain.Chi2Test(mc1665, "WW P CHI2")
#    chi1695 = mcmain.Chi2Test(mc1695, "WW P CHI2")
#    chi1715 = mcmain.Chi2Test(mc1715, "WW P CHI2")
#    chi1735 = mcmain.Chi2Test(mc1735, "WW P CHI2")
#    chi1755 = mcmain.Chi2Test(mc1755, "WW P CHI2")
#    chi1785 = mcmain.Chi2Test(mc1785, "WW P CHI2")
    
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
