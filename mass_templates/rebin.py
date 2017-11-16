#!/usr/bin/env python
from ROOT import TFile, TLegend, TCanvas, gROOT, kOrange, kBlack, kBlue, kCyan, kViolet, kGreen, kRed, TLatex, TGraph, TGraphAsymmErrors, TPad
from ROOT import gStyle
from array import array
from math import sqrt
from argparse import ArgumentParser
import sys
gStyle.SetOptStat("imr")

colors = [kRed, kOrange+1, kGreen+1, kBlack, kCyan, kBlue, kViolet-1]




def rebin_histo(histo, nq):
    # Returns a rebinned histogram with nq bins determined by GetQuantiles
    if nq > histo.GetNbinsX():
	print "Can't rebin to a larger number of bins!"
	return None
    
    if nq == 0:
	return None

    xq = array('d', [0.] * (nq+1))  # Input range from [0 ... 1]
    yq = array('d', [0.] * (nq+1))  # Output quantiles
    for i in range(nq+1): xq[i] = float(i)/float(nq)
    histo.GetQuantiles(nq+1, yq, xq)
    
    print "xq =", xq
    print "yq =", yq

    print "Before rebinning: nbins =", histo.GetNbinsX(), "\tIntegral = ", histo.Integral()
    rebinned = histo.Rebin(nq, histo.GetName() + "_rebinned", yq)
    print "After rebinning: nbins =", rebinned.GetNbinsX(), "\tIntegral = ", rebinned.Integral()
    
    rb_scaled = rebinned.Clone()
    rb_scaled.SetDirectory(0)
    
    # Scale by bin width
    for b in range(rb_scaled.GetNbinsX() + 1):
	    width = rb_scaled.GetXaxis().GetBinWidth(b)
	    rb_scaled.SetBinContent(b, rb_scaled.GetBinContent(b) / width)
    rb_scaled.SetBinError(b, rb_scaled.GetBinError(b) / width)
    print "After scaling by bin width: nbins =", rb_scaled.GetNbinsX(), "\tIntegral = ", rb_scaled.Integral()
    return rebinned, rb_scaled


def plot_templates(templates, title, outF):
    cv = TCanvas(outF + "_templates", "cv", 1600, 1400)
    template_rootF = TFile.Open(outF + ".root", "RECREATE")
    p1 = TPad('p1','p1',0.0,0.95,1.0,0.0)
    p1.Draw()
    p1.SetRightMargin(0.05)
    p1.SetLeftMargin(0.12)
    p1.SetTopMargin(0.01)
    p1.SetBottomMargin(0.25)
    p1.SetGridx(True)
    p1.cd()

    for h in templates:
	h.Write()
    template_rootF.Close()

    
    l = TLegend(0.75, 0.75, 0.95, 0.95)
    l.AddEntry(templates[0], "m_{t} = 166.5 GeV")
    l.AddEntry(templates[1], "m_{t} = 169.5 GeV")
    l.AddEntry(templates[2], "m_{t} = 171.5 GeV")
    l.AddEntry(templates[3], "m_{t} = 172.5 GeV")
    l.AddEntry(templates[4], "m_{t} = 173.5 GeV")
    l.AddEntry(templates[5], "m_{t} = 175.5 GeV")
    l.AddEntry(templates[6], "m_{t} = 178.5 GeV")

    templates[0].GetYaxis().SetTitleOffset(1.5)
    templates[0].GetYaxis().SetTitle("Normalized entries / bin")
    templates[0].Draw("H HIST 9")
    for i, h in enumerate(templates):
	if i is 0: 
	    continue
	h.Draw("SAME H HIST 9")
    l.Draw()

    p2 = TPad('p2','p2',0.0,0.02,1.0,0.17)
    p2.Draw()
    p2.SetBottomMargin(0.01)
    p2.SetRightMargin(0.05)
    p2.SetLeftMargin(0.12)
    p2.SetTopMargin(0.05)
    p2.SetGridx(True)
    p2.SetGridy(True)
    p2.cd()
    gStyle.SetOptStat(0)
    ratioframe=(templates[3]).Clone('ratioframe')
    ratioframe.SetTitle("")
    ratioframe.GetYaxis().SetTitle('ratio to 172.5')
    ratioframe.GetYaxis().SetRangeUser(0.7,1.3)
    ratioframe.GetYaxis().SetNdivisions(5)
    ratioframe.GetYaxis().SetLabelSize(0.18)        
    ratioframe.GetYaxis().SetTitleSize(0.2)
    ratioframe.GetYaxis().SetTitleOffset(0.2)
    ratioframe.GetXaxis().SetLabelSize(0)
    ratioframe.GetXaxis().SetTitleSize(0)
    ratioframe.GetXaxis().SetTitleOffset(0)
    ratioframe.Draw("SAME")

    try:
	gr_list = []
	for rbs in templates:
	    ratio=(templates[3]).Clone('ratio')
	    ratio.SetDirectory(0)
	    ratio.Divide(rbs)
	    gr=TGraphAsymmErrors(ratio)
	    gr.SetMarkerStyle(rbs.GetMarkerStyle())
	    gr.SetMarkerSize(rbs.GetMarkerSize())
	    gr.SetMarkerColor(rbs.GetMarkerColor())
	    gr.SetLineColor(rbs.GetLineColor())
	    gr.SetLineWidth(rbs.GetLineWidth())
	    #gr.SetOptStat(0)
	    gr_list.append(gr)

	for g in gr_list:
	    g.Draw("SAME p ")
    except:
	pass

    cv.SaveAs(outF + ".png")






mass = [166.5, 169.5, 171.5, 173.5, 175.5, 178.5]
#chi2s = [chi1665, chi1695, chi1715, chi1735, chi1755, chi1785]

def graphChi2(nom, mc, masses, nom_mt, name):

    print "====================="
    print "Chi2 values for mt =", nom_mt
    
    gr = TGraph()
    gStyle.SetMarkerColor(kBlue)
    gStyle.SetLineColor(kBlue)
    for i, m in enumerate(masses):
	if not CHI2_include_nomMass:
	    # Don't calculate chi2 with nominal mass included (should evaluate to 0 in that case)
	    if abs(nom_mt - m) < 0.01:
		continue
	mass = str(m)
	np=gr.GetN()
	chi2 = float(nom.Chi2Test(mc[i], "WW  CHI2"))
	gr.SetPoint(np,m,chi2)
	print chi2
    gr.SetMarkerStyle(22)
    gr.Fit('pol2')
    gr.Draw('AP PLC PMC')
    print "====================="
    pol2 = gr.GetFunction("pol2")
    minx = pol2.GetMinimumX(166,188)
    print minx
    miny = pol2.GetMinimum(166,188)
    print miny
    by = miny +1
    print 'by%f'%by

    p0 = pol2.GetParameter(0)
    p1 = pol2.GetParameter(1)
    p2 = pol2.GetParameter(2)
    print p0
    print p1
    print p2
    p0 = p0- by
    b = (-p1-sqrt(p1**2-4*p2*p0))
    print b/(2*p2)
    b = minx - b/(2*p2)
    print b
    c = (-p1+sqrt(p1**2-4*p2*p0))
    print c/(2*p2)
    c = c/(2*p2) - minx
    print c

    c1 = TCanvas('c1','c1')
    gStyle.SetCanvasDefH(600);
    gStyle.SetCanvasDefW(600);
    c1.SetLeftMargin(0.15);
    c1.SetRightMargin(0.25)
    c1.SetBottomMargin(0.25);
    pad1=TPad('p1','p1',0.,0.,1.0,1.0)
    pad1.Draw()

    tlat3 = TLatex()
    tlat3.SetNDC()
    tlat3.SetTextFont(42)
    tlat3.SetTextSize(0.03)
    tlat3.SetTextAlign(31)
    tlat3.DrawLatex(0.8,0.24,'Fit Results')
    tlat3.DrawLatex(0.8,0.19,'m_{t}=%.2f'%(minx))
    #tlat3.DrawLatex(0.8,0.19,'m_{t}=%.2f + %.2f - %.2f'%(minx,b,c))

    pad1.cd()
    gr.GetXaxis().SetTitle("m_{t} [GeV]")
    gr.GetYaxis().SetTitle("\chi^{2}(m_{t})")

    gr.Draw("AP")
    txt=TLatex()
    txt.SetNDC(True)
    txt.SetTextFont(43)
    txt.SetTextSize(20)
    txt.SetTextAlign(12)
    txt.DrawLatex(0.18,0.92,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (35.9) )
    c1.SaveAs(name + ".png")

def main():
    #gROOT.SetBatch(True)  # True: Don't display canvas
    parser = ArgumentParser()
    parser.add_argument("--path", default="1bjet_cut",help="path to directory of histogram files")
    parser.add_argument("--dist", "-d", default="pt_ll", help="kinematic distribution to analyze")
    parser.add_argument("--nbins", "-n", type=int, default=0, help="number of bins to use for rebinning")
    args = parser.parse_args()

    loc = args.path
    if loc[-1] != '/':
	loc += '/'




    # tt histos
    tt_h = []
    tt_files = ["tt/mc_TT_mt1665.root", "tt/mc_TT_mt1695.root", "tt/mc_TT_mt1715.root", \
		    "tt/mc_TT.root", "tt/mc_TT_mt1735.root", "tt/mc_TT_mt1755.root", "tt/mc_TT_mt1785.root"]
    for ttF in tt_files:
	f = TFile.Open(loc + ttF)
	h_tmp = f.Get(args.dist)
	h_tmp.SetDirectory(0)
	tt_h.append(h_tmp)
	f.Close()



    tt_h[0].SetLineColor(kRed)
    tt_h[1].SetLineColor(kOrange+1)
    tt_h[2].SetLineColor(kGreen+1)
    tt_h[3].SetLineColor(kBlack)
    tt_h[4].SetLineColor(kCyan)
    tt_h[5].SetLineColor(kBlue)
    tt_h[6].SetLineColor(kViolet-1)

    for h in tt_h:
	h.SetLineWidth(2)


    x,y = rebin_histo(tt_h[3], args.nbins)

    canv = TCanvas("c","c",700,700)
    x.Draw("H HIST")

    sig = []
    for tth in tt_h:
	sig.append(tth.Clone())

if __name__ == "__main__":
    sys.exit(main())
