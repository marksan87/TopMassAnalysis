#!/usr/bin/env python
from ROOT import TFile, TLegend, TCanvas, gROOT, kOrange, kBlack, kBlue, kCyan, kViolet, kGreen, kRed, TLatex, TGraph, TGraphErrors, TGraphAsymmErrors, TPad
from ROOT import gStyle
from array import array
from math import sqrt
from argparse import ArgumentParser
import sys
gStyle.SetOptStat("imr")

colors = [kRed, kOrange+1, kGreen+1, kBlack, kCyan, kBlue, kViolet-1]


def rebin_histo(histo, nq):
    # Returns a reinned histogram with nq bins determined by GetQuantiles
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






mass = [166.5, 169.5, 171.5, 172.5, 173.5, 175.5, 178.5]

def graphMoments(mean, var, masses):
    print "====================="
    print "Moments"
    
    meanG = TGraphAsymmErrors()
    varG = TGraphAsymmErrors()
    gStyle.SetMarkerColor(kBlue)
    gStyle.SetLineColor(kBlue)
    for i, m in enumerate(masses):
	mass = str(m)
	np=meanG.GetN()
	meanG.SetPoint(np, m, mean[i][0])
	meanG.SetPointError(np, 0., 0., mean[i][1]/2.0, mean[i][1]/2.0)
	varG.SetPoint(np, m, var[i][0])
	varG.SetPointError(np, 0., 0., var[i][1]/2.0, var[i][1]/2.0)
    meanG.SetMarkerStyle(22)
    meanG.Fit('pol1')
    #meanG.Draw('AP PLC PMC')
    print "====================="

    c1 = TCanvas('c1','c1')
    gStyle.SetCanvasDefH(600);
    gStyle.SetCanvasDefW(600);
    c1.SetLeftMargin(0.15);
    c1.SetRightMargin(0.25)
    c1.SetBottomMargin(0.25);
    pad1=TPad('p1','p1',0.,0.,1.0,1.0)
    pad1.Draw()




    f = meanG.GetFunction("pol1")
    p0 = f.GetParameter(0)
    p0_err = f.GetParError(0)
    p1 = f.GetParameter(1)
    p1_err = f.GetParError(1)
    fitline = "t#bar{t}   offset %.f #pm %.f   slope %.3f #pm %.2f" % (p0, p0_err, p1, p1_err)
    print "moment 1: mt = %f" % ((mean[3][0] - p0) / p1)


    pad1.cd()
    meanG.GetXaxis().SetTitle("m_{t} [GeV]")
    meanG.GetYaxis().SetTitle("O^{1} (p_{T}(ll) [GeV]")
    meanG.GetYaxis().SetTitleOffset(1.3)
    meanG.Draw("AP")
    txt=TLatex()
    txt.SetNDC(True)
    txt.SetTextFont(43)
    txt.SetTextSize(18)
    txt.SetTextAlign(12)
    txt.DrawLatex(0.1,0.93,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (35.9) )
    txt.DrawLatex(0.55,0.93, fitline)
    c1.SaveAs("moment1.png")

    #meanG.Draw('AP PLC PMC')
    
    varG.SetMarkerStyle(22)
    varG.Fit('pol1')
    f2 = varG.GetFunction("pol1")
    p0 = f2.GetParameter(0)
    p0_err = f2.GetParError(0)
    p1 = f2.GetParameter(1)
    p1_err = f2.GetParError(1)
    fitline = "t#bar{t}   offset %.f #pm %.f   slope %.3f #pm %.1f" % (p0, p0_err, p1, p1_err)
    print "moment 2: mt = %f" % ((var[3][0] - p0) / p1)
    
    varG.GetXaxis().SetTitle("m_{t} [GeV]")
    varG.GetYaxis().SetTitle("O^{2} (p_{T}(ll) [GeV^{2}]")
    varG.GetYaxis().SetTitleOffset(1.3)
    varG.Draw("AP")
    txt=TLatex()
    txt.SetNDC(True)
    txt.SetTextFont(43)
    txt.SetTextSize(18)
    txt.SetTextAlign(12)
    txt.DrawLatex(0.1, 0.93,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (35.9) )
    txt.DrawLatex(0.55, 0.93, fitline)
    c1.SaveAs("moment2.png")
    return meanG, varG


def calcMoments(histos):
    mean = []
    var = []
    for h in histos:
	mean.append([h.GetMean(), h.GetMeanError()])
	var.append([(h.GetRMS())**2, 2 * h.GetRMS() * h.GetRMSError()])
    return mean, var	
    


def main():
    #gROOT.SetBatch(True)  # True: Don't display canvas
    parser = ArgumentParser()
    parser.add_argument("--path", default="with_gen",help="path to directory of histogram files")
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

    mean, var = calcMoments(tt_h)
    print "First moments"
    for x in mean: print "%f +- %f" % (x[0], x[1])
    print "\nSecond moments"
    for x in var: print "%f += %f" % (x[0], x[1])

    graphMoments(mean, var, mass) 


if __name__ == "__main__":
    sys.exit(main())
