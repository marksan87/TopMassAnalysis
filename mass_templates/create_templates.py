#!/usr/bin/env python
from ROOT import TFile, TLegend, TCanvas, gROOT, kOrange, kBlack, kBlue, kCyan, kViolet, kGreen, kRed, TLatex, TGraph, TGraphAsymmErrors, TPad
gROOT.ProcessLine('.L ../plugins/th1fmorph.cc+')
from ROOT import th1fmorph, gStyle
from array import array
from math import sqrt
from argparse import ArgumentParser

gStyle.SetOptStat("imr")
gROOT.SetBatch(True)  # True: Don't display canvas

colors = [kRed, kOrange+1, kGreen+1, kBlack, kCyan, kBlue, kViolet-1]


parser = ArgumentParser()
parser.add_argument("path", help="path to directory of histogram files")
args = parser.parse_args()



c = TCanvas("c","c", 1600, 1400)


#loc = "btagsf/"
loc = args.path
if loc[-1] != '/':
    loc += '/'

CHI2_include_nomMass = False 

#loc = "pileup_down/"
# tW histos
f1 = TFile.Open(loc + "tW/mc_ST_tW_antitop_mt1695.root")
f2 = TFile.Open(loc + "tW/mc_ST_tW_antitop_mt1755.root")
f3 = TFile.Open(loc + "tW/mc_ST_tW_antitop.root")

h169 = f1.Get("pt_ll")
h169.SetDirectory(0)   # Detaches hist from TFile so the file can be closed

h175 = f2.Get("pt_ll")
h175.SetDirectory(0)

h172 = f3.Get("pt_ll")
h172.SetDirectory(0)

f1.Close()
f2.Close()
f3.Close()

f1 = TFile.Open(loc + "tW/mc_ST_tW_top_mt1695.root")
f2 = TFile.Open(loc + "tW/mc_ST_tW_top_mt1755.root")
f3 = TFile.Open(loc + "tW/mc_ST_tW_top.root")

h1 = f1.Get("pt_ll")
h1.SetDirectory(0)   

h2 = f2.Get("pt_ll")
h2.SetDirectory(0)

h3 = f3.Get("pt_ll")
h3.SetDirectory(0)

h169.Add(h1)
h175.Add(h2)
h172.Add(h3)

f1.Close()
f2.Close()
f3.Close()


f1 = TFile.Open(loc + "mc_ST_s.root")
st_bck = f1.Get("pt_ll")
st_bck.SetDirectory(0)
f1.Close()

f1 = TFile.Open(loc + "mc_ST_t_antitop.root")
htmp = f1.Get("pt_ll")
htmp.SetDirectory(0)
st_bck.Add(htmp)
f1.Close()

f1 = TFile.Open(loc + "mc_ST_t_top.root")
htmp = f1.Get("pt_ll")
htmp.SetDirectory(0)
st_bck.Add(htmp)
f1.Close()

print "Total ST background events:", st_bck.Integral()

tW_events = (h169.Integral() + h175.Integral() + h172.Integral())/3.0


# tt histos
tt_h = []
tt_files = ["tt/mc_TT_mt1665.root", "tt/mc_TT_mt1695.root", "tt/mc_TT_mt1715.root", \
	    "tt/mc_TT.root", "tt/mc_TT_mt1735.root", "tt/mc_TT_mt1755.root", "tt/mc_TT_mt1785.root"]
for ttF in tt_files:
    f = TFile.Open(loc + ttF)
    h_tmp = f.Get("pt_ll")
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

sig = []
for tth in tt_h:
    sig.append(tth.Clone())

#for h in tt_h:
#    h.Scale(1.0 / h.Integral())

tt_templates = TFile.Open("tt_templates.root", "RECREATE")


p1 = TPad('p1','p1',0.0,0.95,1.0,0.0)
p1.Draw()
p1.SetRightMargin(0.05)
p1.SetLeftMargin(0.12)
p1.SetTopMargin(0.01)
p1.SetBottomMargin(0.25)
p1.SetGridx(True)
p1.cd()

tt_h[0].SetName("tt_mt1665")
tt_h[1].SetName("tt_mt1695")
tt_h[2].SetName("tt_mt1715")
tt_h[3].SetName("tt_mt1725")
tt_h[4].SetName("tt_mt1735")
tt_h[5].SetName("tt_mt1755")
tt_h[6].SetName("tt_mt1785")
for h in tt_h:
    h.Write()
tt_templates.Close()

#print "bin 8 contents for TT:"
#for h in tt_h:
#    print h.GetBinContent(8)

l = TLegend(0.75, 0.75, 0.95, 0.95)
l.AddEntry(tt_h[0], "m_{t} = 166.5 GeV")
l.AddEntry(tt_h[1], "m_{t} = 169.5 GeV")
l.AddEntry(tt_h[2], "m_{t} = 171.5 GeV")
l.AddEntry(tt_h[3], "m_{t} = 172.5 GeV")
l.AddEntry(tt_h[4], "m_{t} = 173.5 GeV")
l.AddEntry(tt_h[5], "m_{t} = 175.5 GeV")
l.AddEntry(tt_h[6], "m_{t} = 178.5 GeV")

tt_h[0].Draw("H HIST 9")
for i, h in enumerate(tt_h):
    if i is 0: continue
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
ratioframe=(tt_h[3]).Clone('ratioframe')
ratioframe.GetYaxis().SetTitle('ratio to nominal')
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
    for rbs in tt_h:
	ratio=(tt_h[3]).Clone('ratio')
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

c.SaveAs("tt_pt_ll.jpg")

f = TFile.Open(loc + "plotter.root")
dirF = f.Get("pt_ll")
data = dirF.Get("pt_ll")
# Background subtraction
data.Add(dirF.Get("pt_ll_Diboson"),-1)
data.Add(dirF.Get("pt_ll_W"),-1)
data.Add(dirF.Get("pt_ll_DY"),-1)
data.Add(dirF.Get("pt_ll_t#bar{t}+V"),-1)
data.Add(st_bck, -1)

mcN = dirF.Get("totalmc")
mcN.Scale(1.0/mcN.Integral())

"""
mc_tot = []
mc_tot_files = ["../NtuplePlotter/plots_mt1665/plots/plotter.root", \
		"../NtuplePlotter/plots_mt1695/plots/plotter.root",
		"../NtuplePlotter/plots_mt1715/plots/plotter.root",
		"../NtuplePlotter/plots_mt1735/plots/plotter.root",
		"../NtuplePlotter/plots_mt1755/plots/plotter.root",
		"../NtuplePlotter/plots_mt1785/plots/plotter.root"]

for mcF in mc_tot_files:
    mcfile = TFile.Open(mcF)
    ht = mcfile.Get("pt_ll/totalmc")
    ht.SetDirectory(0)
    mc_tot.append(ht)
    mcfile.Close()

for mc in mc_tot:
    mc.Scale(1.0/mc.Integral())
"""
data.Scale(1.0/data.Integral())


bins = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
fine_bins = [15.8 + 5.8 * n for n in xrange(0, 22)]
#print fine_bins
bins = fine_bins
nbins = 21
#nbins=10
rbData = data.Rebin(nbins, "data rebinned", array('d',bins))


tW166 = th1fmorph("mt = 166.5", "mt = 166.5", h169, h175, 169.5, 175.5, 166.5, tW_events, 0)
tW171 = th1fmorph("mt = 171.5", "mt = 171.5", h169, h175, 169.5, 175.5, 171.5, tW_events, 0)
tW173 = th1fmorph("mt = 173.5", "mt = 173.5", h169, h175, 169.5, 175.5, 173.5, tW_events, 0)
tW178 = th1fmorph("mt = 178.5", "mt = 178.5", h169, h175, 169.5, 175.5, 178.5, tW_events, 0)



tW_templates = TFile.Open("tW_templates.root", "RECREATE")
tW166.SetName("tW_mt1665")
h169.SetName("tW_mt1695")
tW171.SetName("tW_mt1715")
h172.SetName("tW_mt1725")
tW173.SetName("tW_mt1735")
h175.SetName("tW_mt1755")
tW178.SetName("tW_mt1785")

tW = []
tW.append(tW166.Clone())
tW.append(h169.Clone())
tW.append(tW171.Clone())
tW.append(h172.Clone())
tW.append(tW173.Clone())
tW.append(h175.Clone())
tW.append(tW178.Clone())

rbtW = []
for w_ in tW:
    w_.Scale(1.0/w_.Integral())
    rebin_ = w_.Rebin(nbins, "tW rebinned", array('d', bins))
    rbtW.append(rebin_)
    print "mean:", rebin_.GetMean()


tW166.Write()
h169.Write()
tW171.Write()
h172.Write()
tW173.Write()
h175.Write()
tW178.Write()
tW_templates.Close()


sig[0].Add(tW166)
sig[1].Add(h169)
sig[2].Add(tW171)
sig[3].Add(h172)
sig[4].Add(tW173)
sig[5].Add(h175)
sig[6].Add(tW178)


rbTT = []
for tt in tt_h:
    rbTT.append(tt.Rebin(nbins, "tt rebinned", array('d',bins)))

norm_rebin_TT = []
for tt in tt_h:
    tt.Scale(1.0 / tt.Integral())
    norm_rebin_TT.append(tt.Rebin(nbins, "tt normalized rebinned", array('d',bins)))



rbSig = []
for h in sig:
    h.Scale(1.0/h.Integral())


sig_templates = TFile.Open("sig_templates.root", "RECREATE")
sig[0].SetName("sig_mt1665")
sig[1].SetName("sig_mt1695")
sig[2].SetName("sig_mt1715")
sig[3].SetName("sig_mt1725")
sig[4].SetName("sig_mt1735")
sig[5].SetName("sig_mt1755")
sig[6].SetName("sig_mt1785")


for h in sig:
    h.Write()
sig_templates.Close()
for h in sig:
    rbSig.append(h.Rebin(nbins, "signal rebinned", array('d',bins)))

print "rebinned data:", rbData.GetMean()
print "rebinned mc:"
for x in rbSig:
    print x.GetMean()

c = TCanvas('c','c',1000, 1000)
c.SetBottomMargin(0.0)
c.SetLeftMargin(0.0)
c.SetTopMargin(0)
c.SetRightMargin(0.00)
c.cd()
gStyle.SetTitleX(0.6)
p1 = TPad('p1','p1',0.0,0.95,1.0,0.0)
p1.Draw()
p1.SetRightMargin(0.05)
p1.SetLeftMargin(0.12)
p1.SetTopMargin(0.01)
p1.SetBottomMargin(0.25)
p1.SetGridx(True)
p1.cd()

rbSig[0].Draw("H HIST 9")
for i, h in enumerate(rbSig):
    if i is 0: continue
    h.Draw("SAME H HIST 9")

l.Draw()

txt=TLatex()
txt.SetNDC(True)
txt.SetTextFont(43)
txt.SetTextSize(20)
txt.SetTextAlign(12)
txt.DrawLatex(0.15,0.97,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (35.9) )

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
ratioframe=rbData.Clone('ratioframe')
ratioframe.SetTitle("")
ratioframe.GetYaxis().SetTitle('ratio wrt nom')
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
    for rbs in rbSig:
	ratio=rbData.Clone('ratio')
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
c.SaveAs("signal_pt_ll.jpg")

#for h in rbTT:
#    h.Scale(h.Integral())

############
# Not used

"""
chi1665 = rbTT[3].Chi2Test(rbTT[0], "WW  CHI2")
chi1695 = rbTT[3].Chi2Test(rbTT[1], "WW  CHI2")
chi1715 = rbTT[3].Chi2Test(rbTT[2], "WW  CHI2")
chi1735 = rbTT[3].Chi2Test(rbTT[4], "WW  CHI2")
chi1755 = rbTT[3].Chi2Test(rbTT[5], "WW  CHI2")
chi1785 = rbTT[3].Chi2Test(rbTT[6], "WW  CHI2")

chi1665 = (tt_h[3]).Chi2Test(mc_tot[0], "WW  CHI2")
chi1695 = (tt_h[3]).Chi2Test(mc_tot[1], "WW  CHI2")
chi1715 = (tt_h[3]).Chi2Test(mc_tot[2], "WW  CHI2")
chi1735 = (tt_h[3]).Chi2Test(mc_tot[3], "WW  CHI2")
chi1755 = (tt_h[3]).Chi2Test(mc_tot[4], "WW  CHI2")
chi1785 = (tt_h[3]).Chi2Test(mc_tot[5], "WW  CHI2")

chi1665 = mcN.Chi2Test(mc_tot[0], "WW  CHI2")
chi1695 = mcN.Chi2Test(mc_tot[1], "WW  CHI2")
chi1715 = mcN.Chi2Test(mc_tot[2], "WW  CHI2")
chi1735 = mcN.Chi2Test(mc_tot[3], "WW  CHI2")
chi1755 = mcN.Chi2Test(mc_tot[4], "WW  CHI2")
chi1785 = mcN.Chi2Test(mc_tot[5], "WW  CHI2")

chi1665 = data.Chi2Test(mc_tot[0], "WW  CHI2")
chi1695 = data.Chi2Test(mc_tot[1], "WW  CHI2")
chi1715 = data.Chi2Test(mc_tot[2], "WW  CHI2")
chi1735 = data.Chi2Test(mc_tot[3], "WW  CHI2")
chi1755 = data.Chi2Test(mc_tot[4], "WW  CHI2")
chi1785 = data.Chi2Test(mc_tot[5], "WW  CHI2")

chi1665 = rbData.Chi2Test(rbSig[0], "WW  CHI2")
chi1695 = rbData.Chi2Test(rbSig[1], "WW  CHI2")
chi1715 = rbData.Chi2Test(rbSig[2], "WW  CHI2")
chi1735 = rbData.Chi2Test(rbSig[4], "WW  CHI2")
chi1755 = rbData.Chi2Test(rbSig[5], "WW  CHI2")
chi1785 = rbData.Chi2Test(rbSig[6], "WW  CHI2")
"""

mass = [166.5, 169.5, 171.5, 173.5, 175.5, 178.5]
#chi2s = [chi1665, chi1695, chi1715, chi1735, chi1755, chi1785]

def graphChi2(nom, mc, masses, nom_mt, name):
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
    gr.SetMarkerStyle(22)
    gr.Fit('pol2')
    gr.Draw('AP PLC PMC')

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
    c1.SaveAs(name + ".jpg")

#signal = [rbSig[0], rbSig[1], rbSig[2], rbSig[3], rbSig[4], rbSig[5], rbSig[6]]
#signal = [rbTT[0], rbTT[1], rbTT[2], rbTT[3], rbTT[4], rbTT[5], rbTT[6]]

######
#signal = [norm_rebin_TT[0], norm_rebin_TT[1], norm_rebin_TT[2], norm_rebin_TT[3], norm_rebin_TT[4], norm_rebin_TT[5], norm_rebin_TT[6]]
#signal = [rbTT[0], rbTT[1], rbTT[2], rbTT[3], rbTT[4], rbTT[5], rbTT[6]]
signal = [tt_h[0], tt_h[1], tt_h[2], tt_h[3], tt_h[4], tt_h[5], tt_h[6]]
########

#graphChi2(rbData, signal, mass, "chi2_new")

for y in tt_h:
    print "Int:", y.Integral()

mass = [166.5, 169.5, 171.5, 172.5, 173.5, 175.5, 178.5]
#signal = [rbSig[0], rbSig[1], rbSig[2], rbSig[3], rbSig[4], rbSig[5], rbSig[6]]
graphChi2(signal[1], signal, mass, 169.5, "chi2_169")

mass = [166.5, 169.5, 171.5, 172.5, 173.5, 175.5, 178.5]
#signal = [rbSig[0], rbSig[1], rbSig[2], rbSig[3], rbSig[4], rbSig[5], rbSig[6]]
graphChi2(signal[2], signal, mass, 171.5, "chi2_171")

mass = [166.5, 169.5, 171.5, 172.5, 173.5, 175.5, 178.5]
#signal = [rbSig[0], rbSig[1], rbSig[2], rbSig[3], rbSig[4], rbSig[5], rbSig[6]]
graphChi2(signal[3], signal, mass, 172.5, "chi2_172")

#mass = [166.5, 169.5, 171.5, 172.5, 175.5, 178.5]
#signal = [rbSig[0], rbSig[1], rbSig[2], rbSig[3], rbSig[4], rbSig[5], rbSig[6]]
graphChi2(signal[4], signal, mass, 173.5, "chi2_173")

#mass = [166.5, 169.5, 171.5, 172.5, 173.5, 178.5]
#signal = [rbSig[0], rbSig[1], rbSig[2], rbSig[3], rbSig[4], rbSig[5], rbSig[6]]
graphChi2(signal[5], signal, mass, 175.5, "chi2_175")

#chi1665 = rbData.Chi2Test(rbTT[0], "WW  CHI2")
#chi1695 = rbData.Chi2Test(rbTT[1], "WW  CHI2")
#chi1715 = rbData.Chi2Test(rbTT[2], "WW  CHI2")
#chi1735 = rbData.Chi2Test(rbTT[4], "WW  CHI2")
#chi1755 = rbData.Chi2Test(rbTT[5], "WW  CHI2")
#chi1785 = rbData.Chi2Test(rbTT[6], "WW  CHI2")

"""
chi1695 = mc_tot[0].Chi2Test(mc_tot[1], "WW  CHI2")
chi1715 = mc_tot[0].Chi2Test(mc_tot[2], "WW  CHI2")
chi1665 = mc_tot[0].Chi2Test(mcN, "WW  CHI2")
chi1735 = mc_tot[0].Chi2Test(mc_tot[3], "WW  CHI2")
chi1755 = mc_tot[0].Chi2Test(mc_tot[4], "WW  CHI2")
chi1785 = mc_tot[0].Chi2Test(mc_tot[5], "WW  CHI2")
"""


#chi1665 = data.chi2test(tt_h[0], "ww  chi2")
#chi1695 = data.chi2test(tt_h[1], "ww  chi2")
#chi1715 = data.chi2test(tt_h[2], "ww  chi2")
#chi1735 = data.chi2test(tt_h[4], "ww  chi2")
#chi1755 = data.chi2test(tt_h[5], "ww  chi2")
#chi1785 = data.chi2test(tt_h[6], "ww  chi2")

"""
print "mt = 166.5: chi2 = ", chi1665
print "mt = 169.5: chi2 = ", chi1695
print "mt = 171.5: chi2 = ", chi1715
print "mt = 173.5: chi2 = ", chi1735
print "mt = 175.5: chi2 = ", chi1755
print "mt = 178.5: chi2 = ", chi1785
"""


h169.Scale(1.0 / h169.Integral())
h175.Scale(1.0 / h175.Integral())


h169.SetLineColor(kOrange + 1) 
h172.SetLineColor(kBlack) 
h175.SetLineColor(kBlue)

h166 = th1fmorph("mt = 166.5", "mt = 166.5", h169, h175, 169.5, 175.5, 166.5, 1.0, 0)
h171 = th1fmorph("mt = 171.5", "mt = 171.5", h169, h175, 169.5, 175.5, 171.5, 1.0, 0)
h173 = th1fmorph("mt = 173.5", "mt = 173.5", h169, h175, 169.5, 175.5, 173.5, 1.0, 0)
h178 = th1fmorph("mt = 178.5", "mt = 178.5", h169, h175, 169.5, 175.5, 178.5, 1.0, 0)

h166.SetLineColor(kRed)
h171.SetLineColor(kGreen+1)
h173.SetLineColor(kCyan)
h178.SetLineColor(kViolet - 1)


h169.Draw("H HIST 9")
h175.Draw("SAME H HIST 9")
h166.Draw("SAME H HIST 9")
h171.Draw("SAME H HIST 9")
h172.Draw("SAME H HIST 9")
h173.Draw("SAME H HIST 9")
h178.Draw("SAME H HIST 9")


l = TLegend(0.7, 0.55, 0.9, 0.75)
l.AddEntry(h166, "mt = 166.5 GeV")
l.AddEntry(h169, "mt = 169.5 GeV")
l.AddEntry(h171, "mt = 171.5 GeV")
l.AddEntry(h172, "mt = 172.5 GeV")
l.AddEntry(h173, "mt = 173.5 GeV")
l.AddEntry(h175, "mt = 175.5 GeV")
l.AddEntry(h178, "mt = 178.5 GeV")
l.Draw()



