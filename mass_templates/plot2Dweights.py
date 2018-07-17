#!/usr/bin/env python
import os
from ROOT import *

obsTitle = {"ptll":"p_{T}(ll)", "ptpos":"p_{T}(l^{+})", "Epos":"E(l^{+})", "ptp_ptm":"p_{T}(l^{+}) + p_{T}(l^{-})", "Ep_Em":"E(l^{+}) + E(l^{-})", "Mll":"M(ll)"}

f = TFile.Open("ttrees/tt/mc_TT.root")
t = f.Get("goodEvents")

for d in obsTitle.keys():
    exec("h%s = TH2D('weight_vs_%s', 'Event weight vs rec %s', 100, 20, 250., 100, 0., 0.8)" % (d,d,obsTitle[d]))
    exec("h%s.GetXaxis().SetTitle('%s')" % (d,obsTitle[d]))
    exec("h%s.GetYaxis().SetTitle('Event weight')" % d) 

#h = TH2D("evtWeight_vs_ptll", "Event weight vs rec p_{T}(ll)", 100, 20., 250., 100, 0., 0.8)
#h.GetXaxis().SetTitle("p_{T}(ll) [GeV]")
#h.GetYaxis().SetTitle("Event weight")
#for evt in t:
#    h.Fill(evt.rec_ptll, evt.weight)

for evt in t:
    for d in obsTitle.keys():
        exec("h%s.Fill(evt.rec_%s, evt.weight)" % (d,d))

gStyle.SetOptStat(0)
c = TCanvas("c","c", 1200, 800)
c.SetRightMargin(0.15)

os.system("mkdir -p weight2Dplots")
outF = TFile.Open("weight2Dplots/weight2Dplots.root", "recreate")
for d in obsTitle.keys():
    exec("h%s.Draw('colz')" % d)
    exec("c.SaveAs('weight2Dplots/%s_weights.png')" % d)
    exec("h%s.Write()" % d)
    #h.Draw("colz")

f.Close()
outF.Close()
