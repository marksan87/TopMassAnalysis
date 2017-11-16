#!/usr/bin/env python
from ROOT import TFile, TLegend, TCanvas, gROOT, kOrange, kBlack, kBlue, kCyan, kViolet, kGreen, kRed, TLatex, TGraph, TGraphAsymmErrors, TPad
from ROOT import gStyle
from array import array
from math import sqrt
from argparse import ArgumentParser
from rebin import rebin_histo
import sys
gStyle.SetOptStat("imr")

colors = [kRed, kOrange+1, kGreen+1, kBlack, kCyan, kBlue, kViolet-1]


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

canv = TCanvas("c","c",1000,100)
x.Draw("H HIST")

