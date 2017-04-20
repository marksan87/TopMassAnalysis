#!/usr/bin/env python
from ROOT import TFile, TLegend, TCanvas, gROOT, kOrange, kBlack, kBlue, kCyan, kViolet, kGreen, kRed
gROOT.ProcessLine('.L ../plugins/th1fmorph.cc+')
from ROOT import th1fmorph, gStyle

gStyle.SetOptStat("imr")
gROOT.SetBatch(True)  # True: Don't display canvas

colors = [kRed, kOrange+1, 

c = TCanvas("c","c", 1400, 1400)

# tW histos
f1 = TFile.Open("tW/mc_ST_tW_antitop_mt1695.root")
f2 = TFile.Open("tW/mc_ST_tW_antitop_mt1755.root")
f3 = TFile.Open("tW/mc_ST_tW_antitop.root")

h169 = f1.Get("pt_ll")
h169.SetDirectory(0)   # Detaches hist from TFile so the file can be closed

h175 = f2.Get("pt_ll")
h175.SetDirectory(0)

h172 = f3.Get("pt_ll")
h172.SetDirectory(0)

f1.Close()
f2.Close()
f3.Close()

f1 = TFile.Open("tW/mc_ST_tW_top_mt1695.root")
f2 = TFile.Open("tW/mc_ST_tW_top_mt1755.root")
f3 = TFile.Open("tW/mc_ST_tW_top.root")

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


# tt histos
tt_h = []
tt_files = ["tt/mc_TT_mt1665.root", "tt/mc_TT_mt1695.root", "tt/mc_TT_mt1715.root", \
	    "tt/mc_TT.root", "tt/mc_TT_mt1735.root", "tt/mc_TT_mt1755.root", "tt/mc_TT/mt1785.root"]
for ttF in tt_files:
    f = TFile.Open(ttF)
    h_tmp = f.Get("pt_ll")
    h_tmp.SetDirectory(0)
    tt_h.append(h_tmp)
    f.Close()





h169.Scale(1.0 / h169.Integral())
h175.Scale(1.0 / h175.Integral())

l = TLegend(0.7, 0.55, 0.9, 0.75)

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


l.AddEntry(h166, "mt = 166.5 GeV")
l.AddEntry(h169, "mt = 169.5 GeV")
l.AddEntry(h171, "mt = 171.5 GeV")
l.AddEntry(h172, "mt = 172.5 GeV")
l.AddEntry(h173, "mt = 173.5 GeV")
l.AddEntry(h175, "mt = 175.5 GeV")
l.AddEntry(h178, "mt = 178.5 GeV")
l.Draw()

c.SaveAs("tW_pt_ll.jpg")

