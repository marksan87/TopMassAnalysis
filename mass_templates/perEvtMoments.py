#!/usr/bin/env python
from ROOT import TFile, TLegend, TCanvas, gROOT, kOrange, kBlack, kBlue, kCyan, kViolet, kGreen, kRed, TLatex, TGraph, TGraphErrors, TGraphAsymmErrors, TPad
from ROOT import gStyle
from array import array
from math import sqrt
from argparse import ArgumentParser
import sys
import os
import pickle
gStyle.SetOptStat("imr")

colors = [kRed, kOrange+1, kGreen+1, kBlack, kCyan, kBlue, kViolet-1]
MASSES = [166.5, 169.5, 171.5, 172.5, 173.5, 175.5, 178.5]
obsTitle = {"ptll":"p_{T}(ll)", "ptpos":"p_{T}(l^{+})", "Epos":"E(l^{+})", "ptp_ptm":"p_{T}(l^{+}) + p_{T}(l^{-})", "Ep_Em":"E(l^{+}) + E(l^{-})", "Mll":"M(ll)"}
gROOT.SetBatch(True)

def graphMoments(m1_rec, m1_gen, m2_rec, m2_gen, obs, masses):
    outDir = "unbinnedMoments/%s" % obs
    os.system("mkdir -p %s" % outDir)
    print "====================="
    print "Moments"
    
    m1_recG = TGraphAsymmErrors()
    m1_genG = TGraphAsymmErrors()
    m2_recG = TGraphAsymmErrors()
    m2_genG = TGraphAsymmErrors()
    gStyle.SetMarkerColor(kBlue)
    gStyle.SetLineColor(kBlack)
    for i, m in enumerate(masses):
        mass = str(m)
        np=m1_recG.GetN()
        m1_recG.SetPoint(np, m, m1_rec[i][0])
        m1_recG.SetPointError(np, 0., 0., m1_rec[i][1], m1_rec[i][1])
        m1_genG.SetPoint(np, m, m1_gen[i][0])
        m1_genG.SetPointError(np, 0., 0., m1_gen[i][1], m1_gen[i][1])
        
        m2_recG.SetPoint(np, m, m2_rec[i][0])
        m2_recG.SetPointError(np, 0., 0., m2_rec[i][1], m2_rec[i][1])
        m2_genG.SetPoint(np, m, m2_gen[i][0])
        m2_genG.SetPointError(np, 0., 0., m2_gen[i][1], m2_gen[i][1])
        
        m1_recG.SetMarkerStyle(22)
        m1_recG.Fit('pol1')
        m1_genG.SetMarkerStyle(22)
        m1_genG.Fit('pol1')
    print "====================="


    m1_recG.SetTitle("%s rec" % obsTitle[obs])
    m1_recG.SetName("%s_rec" % obs)
    m1_genG.SetTitle("%s gen" % obsTitle[obs])
    m1_genG.SetName("%s_gen" % obs)
    m2_recG.SetTitle("%s rec" % obsTitle[obs])
    m2_recG.SetName("%s_rec" % obs)
    m2_genG.SetTitle("%s gen" % obsTitle[obs])
    m2_genG.SetName("%s_gen" % obs)


    c1 = TCanvas('c1','c1', 1200, 800)
    #gStyle.SetCanvasDefH(600);
    #gStyle.SetCanvasDefW(600);
    gStyle.SetTitleFontSize(0.04)
    c1.SetLeftMargin(0.15);
    c1.SetRightMargin(0.25)
    c1.SetBottomMargin(0.25);
    #pad1=TPad('p1','p1',0.05,0.05,0.95,0.95)
    pad1=TPad('p1','p1',0.,0.,1.,0.97)
    pad1.Draw()




    f1rec = m1_recG.GetFunction("pol1")
    p0 = f1rec.GetParameter(0)
    p0_err = f1rec.GetParError(0)
    p1 = f1rec.GetParameter(1)
    p1_err = f1rec.GetParError(1)
    fitline = "t#bar{t}   offset %.f #pm %.f   slope %.3f #pm %.2f" % (p0, p0_err, p1, p1_err)
    
    mu = m1_rec[3][0]
    mu_err = m1_rec[3][1]
    mt_m1_rec = (mu - p0) / p1
    mt_m1_rec_err = mu_err / p1
    print "rec moment 1: mt = %f +- %f\tp0: %f\tp1: %f" % (mt_m1_rec, mt_m1_rec_err, p0, p1)


    pad1.cd()
    m1_recG.GetXaxis().SetTitle("m_{t} [GeV]")
    m1_recG.GetYaxis().SetTitle("O^{1} %s [GeV]" % obsTitle[obs])
    m1_recG.GetYaxis().SetTitleOffset(1.3)
    m1_recG.Draw("AP")
    txt=TLatex()
    txt.SetNDC(True)
    txt.SetTextFont(43)
    txt.SetTextSize(20)
    txt.SetTextAlign(12)
    txt.DrawLatex(0.1,0.92,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (35.9) )
    txt.DrawLatex(0.55,0.92, fitline)
    txt.DrawLatex(0.6, 0.22, "m_{t} = %.2f #pm %.2f (stat) [GeV]" % (mt_m1_rec, mt_m1_rec_err))

    c1.SaveAs("unbinnedMoments/%s/m1_rec_%s.png" % (obs,obs))
   

    f1gen = m1_genG.GetFunction("pol1")
    p0 = f1gen.GetParameter(0)
    p0_err = f1gen.GetParError(0)
    p1 = f1gen.GetParameter(1)
    p1_err = f1gen.GetParError(1)
    fitline = "t#bar{t}   offset %.f #pm %.f   slope %.3f #pm %.2f" % (p0, p0_err, p1, p1_err)
    
    mu = m1_gen[3][0]
    mu_err = m1_gen[3][1]
    mt_m1_gen = (mu - p0) / p1
    mt_m1_gen_err = mu_err / p1
    print "gen moment 1: mt = %f +- %f\tp0: %f\tp1: %f" % (mt_m1_gen, mt_m1_gen_err, p0, p1)


    pad1.cd()
    m1_genG.SetTitle("%s gen" % obsTitle[obs])
    m1_genG.GetXaxis().SetTitle("m_{t} [GeV]")
    m1_genG.GetYaxis().SetTitle("O^{1} %s [GeV]" % obsTitle[obs])
    m1_genG.GetYaxis().SetTitleOffset(1.3)
    m1_genG.Draw("AP")
    txt.DrawLatex(0.1,0.92,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (35.9) )
    txt.DrawLatex(0.55,0.92, fitline)
    txt.DrawLatex(0.6, 0.22, "m_{t} = %.2f #pm %.2f (stat) [GeV]" % (mt_m1_gen, mt_m1_gen_err))
    c1.SaveAs("unbinnedMoments/%s/m1_gen_%s.png" % (obs,obs))




    # Moment 2

    m2_recG.SetMarkerStyle(22)
    m2_recG.Fit('pol1')
    f2rec = m2_recG.GetFunction("pol1")
    p0 = f2rec.GetParameter(0)
    p0_err = f2rec.GetParError(0)
    p1 = f2rec.GetParameter(1)
    p1_err = f2rec.GetParError(1)
    fitline = "t#bar{t}   offset %.f #pm %.f   slope %.3f #pm %.1f" % (p0, p0_err, p1, p1_err)
    
    mu = m2_rec[3][0]
    mu_err = m2_rec[3][1]
    mt_m2_rec = (mu - p0) / p1
    mt_m2_rec_err = mu_err / p1
    print "rec moment 2: mt = %f +- %f\tp0: %f\tp1: %f" % (mt_m2_rec, mt_m2_rec_err, p0, p1)
   
    pad1.cd()
    m2_recG.GetXaxis().SetTitle("m_{t} [GeV]")
    m2_recG.GetYaxis().SetTitle("O^{2} %s [GeV^{2}]" % obsTitle[obs])
    m2_recG.GetXaxis().SetTitleOffset(1.)
    m2_recG.GetYaxis().SetTitleOffset(1.3)
    m2_recG.Draw("AP")
    txt.DrawLatex(0.1, 0.92,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (35.9) )
    txt.DrawLatex(0.55, 0.92, fitline)
    txt.DrawLatex(0.6, 0.22, "m_{t} = %.2f #pm %.2f (stat) [GeV]" % (mt_m2_rec, mt_m2_rec_err))
    c1.SaveAs("unbinnedMoments/%s/m2_rec_%s.png" % (obs,obs))
    
    
    m2_genG.SetMarkerStyle(22)
    m2_genG.Fit('pol1')
    f2gen = m2_genG.GetFunction("pol1")
    p0 = f2gen.GetParameter(0)
    p0_err = f2gen.GetParError(0)
    p1 = f2gen.GetParameter(1)
    p1_err = f2gen.GetParError(1)
    fitline = "t#bar{t}   offset %.f #pm %.f   slope %.3f #pm %.1f" % (p0, p0_err, p1, p1_err)
    
    mu = m2_gen[3][0]
    mu_err = m2_gen[3][1]
    mt_m2_gen = (mu - p0) / p1
    mt_m2_gen_err = mu_err / p1 
    print "gen moment 2: mt = %f +- %f\tp0: %f\tp1: %f" % (mt_m2_gen, mt_m2_gen_err, p0, p1)
    
    pad1.cd()
    m2_genG.GetXaxis().SetTitle("m_{t} [GeV]")
    m2_genG.GetYaxis().SetTitle("O^{2} %s [GeV^{2}]" % obsTitle[obs])
    m2_genG.GetYaxis().SetTitleOffset(1.3)
    m2_genG.Draw("AP")
    txt.DrawLatex(0.1, 0.92,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (35.9) )
    txt.DrawLatex(0.55, 0.92, fitline)
    txt.DrawLatex(0.6, 0.22, "m_{t} = %.2f #pm %.2f (stat) [GeV]" % (mt_m2_gen, mt_m2_gen_err))
    c1.SaveAs("unbinnedMoments/%s/m2_gen_%s.png" % (obs,obs))

    print "rec moment 1: mt = %f +- %f" % (mt_m1_rec, mt_m1_rec_err)
    print "gen moment 1: mt = %f +- %f" % (mt_m1_gen, mt_m1_gen_err)
    print "rec moment 2: mt = %f +- %f" % (mt_m2_rec, mt_m2_rec_err)
    print "gen moment 2: mt = %f +- %f" % (mt_m2_gen, mt_m2_gen_err)

    outF = TFile.Open(outDir + "/%s_moments.root" % obs, "RECREATE")
    m1_recG.Write()
    m1_genG.Write()
    m2_recG.Write()
    m2_genG.Write()


    outF.Write()
    outF.Close() 
    return m1_recG, m1_genG, m2_recG, m2_genG

    

def calcPerEvtMoments(tree, obs, cut, sys=("",0)):
    totalWeight = 0. 
    # First moments
    m1_rec = 0.
    m1_gen = 0.
    # Second moments
    m2_rec = 0.
    m2_gen = 0.
    # Fourth moments (for calculating uncertainty)
    m4_rec = 0.
    m4_gen = 0.


    s = sys[0]
    sys_m1_rec = [0.] * sys[1]  # Number of systematics
    sys_m1_gen = [0.] * sys[1]
    sys_m2_rec = [0.] * sys[1]
    sys_m2_gen = [0.] * sys[1]
    sys_m4_rec = [0.] * sys[1]
    sys_m4_gen = [0.] * sys[1]
    sysTotalWeight = [0.] * sys[1]
    sys_m1_rec_unc = [0.] * sys[1]
    sys_m1_gen_unc = [0.] * sys[1]
    sys_m2_rec_unc = [0.] * sys[1]
    sys_m2_gen_unc = [0.] * sys[1]
    evts_cut = 0
    
    if sys[0] == "":
        # No systematics
        if cut < 0.:	
            for evt in tree:
                m1_rec += eval("evt.weight * evt.rec_%s" % obs)
                m1_gen += eval("evt.weight * evt.gen_%s" % obs)
                m2_rec += eval("evt.weight * evt.rec_%s ** 2" % obs)
                m2_gen += eval("evt.weight * evt.gen_%s ** 2" % obs)
                m4_rec += eval("evt.weight * evt.rec_%s ** 4" % obs)
                m4_gen += eval("evt.weight * evt.gen_%s ** 4" % obs)
                totalWeight += evt.weight
        else:
            for evt in tree:
                if eval("evt.rec_%s" % obs) > cut: 
                    evts_cut += 1
                    continue
                
                m1_rec += eval("evt.weight * evt.rec_%s" % obs)
                m1_gen += eval("evt.weight * evt.gen_%s" % obs)
                m2_rec += eval("evt.weight * evt.rec_%s ** 2" % obs)
                m2_gen += eval("evt.weight * evt.gen_%s ** 2" % obs)
                m4_rec += eval("evt.weight * evt.rec_%s ** 4" % obs)
                m4_gen += eval("evt.weight * evt.gen_%s ** 4" % obs)
                totalWeight += evt.weight
    
    elif sys[1] == 1:
        # One variation
        if cut < 0.:	
            for evt in tree:
                m1_rec += eval("evt.weight * evt.rec_%s" % obs)
                m1_gen += eval("evt.weight * evt.gen_%s" % obs)
                m2_rec += eval("evt.weight * evt.rec_%s ** 2" % obs)
                m2_gen += eval("evt.weight * evt.gen_%s ** 2" % obs)
                m4_rec += eval("evt.weight * evt.rec_%s ** 4" % obs)
                m4_gen += eval("evt.weight * evt.gen_%s ** 4" % obs)
                sys_m1_rec[0] += eval("evt.weight_%s * evt.rec_%s" % (s,obs))
                sys_m1_gen[0] += eval("evt.weight_%s * evt.gen_%s" % (s,obs))
                sys_m2_rec[0] += eval("evt.weight_%s * evt.rec_%s ** 2" % (s,obs))
                sys_m2_gen[0] += eval("evt.weight_%s * evt.gen_%s ** 2" % (s,obs))
                sys_m4_rec[0] += eval("evt.weight_%s * evt.rec_%s ** 4" % (s,obs))
                sys_m4_gen[0] += eval("evt.weight_%s * evt.gen_%s ** 4" % (s,obs))
                totalWeight += evt.weight
                sysTotalWeight[0] += eval("evt.weight_%s" % s)
        else:
            for evt in tree:
                if eval("evt.rec_%s" % obs) > cut:
                    evts_cut += 1
                    continue
                
                m1_rec += eval("evt.weight * evt.rec_%s" % obs)
                m1_gen += eval("evt.weight * evt.gen_%s" % obs)
                m2_rec += eval("evt.weight * evt.rec_%s ** 2" % obs)
                m2_gen += eval("evt.weight * evt.gen_%s ** 2" % obs)
                m4_rec += eval("evt.weight * evt.rec_%s ** 4" % obs)
                m4_gen += eval("evt.weight * evt.gen_%s ** 4" % obs)
                sys_m1_rec[0] += eval("evt.weight_%s * evt.rec_%s" % (s,obs))
                sys_m1_gen[0] += eval("evt.weight_%s * evt.gen_%s" % (s,obs))
                sys_m2_rec[0] += eval("evt.weight_%s * evt.rec_%s ** 2" % (s,obs))
                sys_m2_gen[0] += eval("evt.weight_%s * evt.gen_%s ** 2" % (s,obs))
                sys_m4_rec[0] += eval("evt.weight_%s * evt.rec_%s ** 4" % (s,obs))
                sys_m4_gen[0] += eval("evt.weight_%s * evt.gen_%s ** 4" % (s,obs))
                totalWeight += evt.weight
                sysTotalWeight[0] += eval("evt.weight_%s" % s)
    
    elif sys[1] == 2:
        # Include both 'Up' and 'Down'
        if cut < 0.:	
            for evt in tree:
                m1_rec += eval("evt.weight * evt.rec_%s" % obs)
                m1_gen += eval("evt.weight * evt.gen_%s" % obs)
                m2_rec += eval("evt.weight * evt.rec_%s ** 2" % obs)
                m2_gen += eval("evt.weight * evt.gen_%s ** 2" % obs)
                m4_rec += eval("evt.weight * evt.rec_%s ** 4" % obs)
                m4_gen += eval("evt.weight * evt.gen_%s ** 4" % obs)
                
                # Sys up
                sys_m1_rec[0] += eval("evt.weight_%sUp * evt.rec_%s" % (s,obs))
                sys_m1_gen[0] += eval("evt.weight_%sUp* evt.gen_%s" % (s,obs))
                sys_m2_rec[0] += eval("evt.weight_%sUp* evt.rec_%s ** 2" % (s,obs))
                sys_m2_gen[0] += eval("evt.weight_%sUp* evt.gen_%s ** 2" % (s,obs))
                sys_m4_rec[0] += eval("evt.weight_%sUp* evt.rec_%s ** 4" % (s,obs))
                sys_m4_gen[0] += eval("evt.weight_%sUp* evt.gen_%s ** 4" % (s,obs))
                
                # Sys down
                sys_m1_rec[1] += eval("evt.weight_%sDown * evt.rec_%s" % (s,obs))
                sys_m1_gen[1] += eval("evt.weight_%sDown * evt.gen_%s" % (s,obs))
                sys_m2_rec[1] += eval("evt.weight_%sDown * evt.rec_%s ** 2" % (s,obs))
                sys_m2_gen[1] += eval("evt.weight_%sDown * evt.gen_%s ** 2" % (s,obs))
                sys_m4_rec[1] += eval("evt.weight_%sDown * evt.rec_%s ** 4" % (s,obs))
                sys_m4_gen[1] += eval("evt.weight_%sDown * evt.gen_%s ** 4" % (s,obs))
                totalWeight += evt.weight
                sysTotalWeight[0] += eval("evt.weight_%sUp" % s)
                sysTotalWeight[1] += eval("evt.weight_%sDown" % s)
        else:
            for evt in tree:
                if eval("evt.rec_%s" % obs) > cut:
                    evts_cut += 1
                    continue
                
                m1_rec += eval("evt.weight * evt.rec_%s" % obs)
                m1_gen += eval("evt.weight * evt.gen_%s" % obs)
                m2_rec += eval("evt.weight * evt.rec_%s ** 2" % obs)
                m2_gen += eval("evt.weight * evt.gen_%s ** 2" % obs)
                m4_rec += eval("evt.weight * evt.rec_%s ** 4" % obs)
                m4_gen += eval("evt.weight * evt.gen_%s ** 4" % obs)
                
                # Sys up
                sys_m1_rec[0] += eval("evt.weight_%sUp * evt.rec_%s" % (s,obs))
                sys_m1_gen[0] += eval("evt.weight_%sUp* evt.gen_%s" % (s,obs))
                sys_m2_rec[0] += eval("evt.weight_%sUp* evt.rec_%s ** 2" % (s,obs))
                sys_m2_gen[0] += eval("evt.weight_%sUp* evt.gen_%s ** 2" % (s,obs))
                sys_m4_rec[0] += eval("evt.weight_%sUp* evt.rec_%s ** 4" % (s,obs))
                sys_m4_gen[0] += eval("evt.weight_%sUp* evt.gen_%s ** 4" % (s,obs))
                
                # Sys down
                sys_m1_rec[1] += eval("evt.weight_%sDown * evt.rec_%s" % (s,obs))
                sys_m1_gen[1] += eval("evt.weight_%sDown * evt.gen_%s" % (s,obs))
                sys_m2_rec[1] += eval("evt.weight_%sDown * evt.rec_%s ** 2" % (s,obs))
                sys_m2_gen[1] += eval("evt.weight_%sDown * evt.gen_%s ** 2" % (s,obs))
                sys_m4_rec[1] += eval("evt.weight_%sDown * evt.rec_%s ** 4" % (s,obs))
                sys_m4_gen[1] += eval("evt.weight_%sDown * evt.gen_%s ** 4" % (s,obs))
                totalWeight += evt.weight
                sysTotalWeight[0] += eval("evt.weight_%sUp" % s)
                sysTotalWeight[1] += eval("evt.weight_%sDown" % s)
    
    m1_rec /= totalWeight
    m1_gen /= totalWeight
    m2_rec /= totalWeight
    m2_gen /= totalWeight
    m4_rec /= totalWeight
    m4_gen /= totalWeight

    m1_rec_unc = ( (m2_rec - m1_rec**2) / totalWeight)**0.5
    m1_gen_unc = ( (m2_gen - m1_gen**2) / totalWeight)**0.5
    m2_rec_unc = ( (m4_rec - m2_rec**2) / totalWeight)**0.5
    m2_gen_unc = ( (m4_gen - m2_gen**2) / totalWeight)**0.5

    for i in xrange(sys[1]):
        sys_m1_rec[i] /= sysTotalWeight[i]
        sys_m1_gen[i] /= sysTotalWeight[i]
        sys_m2_rec[i] /= sysTotalWeight[i]
        sys_m2_gen[i] /= sysTotalWeight[i]
        sys_m4_rec[i] /= sysTotalWeight[i]
        sys_m4_gen[i] /= sysTotalWeight[i]

        sys_m1_rec_unc[i] = ( (sys_m2_rec[i] - sys_m1_rec[i]**2) / sysTotalWeight[i])**0.5
        sys_m1_gen_unc[i] = ( (sys_m2_gen[i] - sys_m1_gen[i]**2) / sysTotalWeight[i])**0.5
        sys_m2_rec_unc[i] = ( (sys_m4_rec[i] - sys_m2_rec[i]**2) / sysTotalWeight[i])**0.5
        sys_m2_gen_unc[i] = ( (sys_m4_gen[i] - sys_m2_gen[i]**2) / sysTotalWeight[i])**0.5
            

    print "Total Events:", totalWeight 
    if sys[0] == "":
        return [m1_rec, m1_rec_unc], [m1_gen, m1_gen_unc], [m2_rec, m2_rec_unc], [m2_gen, m2_gen_unc], evts_cut
    else:
        return [m1_rec, m1_rec_unc], [m1_gen, m1_gen_unc], [m2_rec, m2_rec_unc], [m2_gen, m2_gen_unc], evts_cut, [sys_m1_rec,sys_m1_rec_unc], [sys_m1_gen, sys_m1_gen_unc], [sys_m2_rec, sys_m2_rec_unc], [sys_m2_gen, sys_m2_gen_unc]


def main():
    #gROOT.SetBatch(True)  # True: Don't display canvas
    parser = ArgumentParser()
    #parser.add_argument("--path", default="../NtuplePlotter/plots2018",help="path to directory of histogram files")
    parser.add_argument("--path", default="ttrees/tt/",help="path to directory of histogram files")
    parser.add_argument("--obs", "-d", default="ptll", help="kinematic distribution to analyze")
    parser.add_argument("--cut", "-c", default = 180, help="upper limiit to cut on", type=float)
    parser.add_argument("-s", "--sys", default = "", help="systematic to test")
    parser.add_argument("-o", "--outDir", default="unbinnedMoments", help="directory to output files to")
    parser.add_argument("-p", "--pkl", default = "", help="plot moments from pickle file")
    args = parser.parse_args()

    loc = args.path
    if loc[-1] != '/':
	loc += '/'




    # tt histos
    tt_trees = []
    tt_files = ["mc_TT-mt1665.root", "mc_TT-mt1695.root", "mc_TT-mt1715.root", \
		    "mc_TT-mt1725.root", "mc_TT-mt1735.root", "mc_TT-mt1755.root", "mc_TT-mt1785.root"]
    #tt_files = ["mc_TT_mt1725.root"]

    f = [None for i in xrange(7)]
    for i, ttF in enumerate(tt_files):
	f[i] = TFile.Open(loc + ttF)
	t_tmp = f[i].Get('goodEvents')
#	t_tmp.SetDirectory(0)
	tt_trees.append(t_tmp)
#	f.Close()

    m1_rec = []
    m1_gen = []
    m2_rec = []
    m2_gen = []
    sysUp_m1_rec = []
    sysUp_m1_gen = []
    sysUp_m2_rec = []
    sysUp_m2_gen = []
    sysDn_m1_rec = []
    sysDn_m1_gen = []
    sysDn_m2_rec = []
    sysDn_m2_gen = []
    weights = []

    if args.pkl == "":
        for i, tree in enumerate(tt_trees):
            print "Processing file %s" % tt_files[i]
            # Each var returned is a list: [val, error]
            if args.sys == "":
                m1_r, m1_g, m2_r, m2_g, evts_cut = calcPerEvtMoments(tree, args.obs, args.cut, (args.sys,0))
            else:
                m1_r, m1_g, m2_r, m2_g, evts_cut, sys_m1_r, sys_m1_g, sys_m2_r, sys_m2_g = calcPerEvtMoments(tree, args.obs, args.cut, (args.sys, 1 if args.sys == "TopPtReweight" else 2))

            """
            m1_r = [i,  i/5.]
            m1_g = [i,  i/5.]
            m2_r = [i,  i/5.]
            m2_g = [i,  i/5.]
            evts_cut = 0
            """
            
            m1_rec.append(m1_r)
            m1_gen.append(m1_g)
            m2_rec.append(m2_r)
            m2_gen.append(m2_g)
            print "mt = %.1f\tEvents cut (> %.f): %d" % (MASSES[i], args.cut, evts_cut)
            
            print "rec: m1 = %f +- %f\tm2 = %f +- %f" % (m1_r[0], m1_r[1], m2_r[0], m2_r[1])
            print "gen: m1 = %f +- %f\tm2 = %f +- %f" % (m1_g[0], m1_g[1], m2_g[0], m2_g[1])
        
            if args.sys != "":
                # sys[a][b]
                # a = 0: val    a = 1: unc
                # b = 0: Up     b = 1: Down
                sysUp_m1_r = sys_m1_r[0][0]
                sysUp_m1_r_unc = sys_m1_r[1][0]
                sysUp_m1_rec.append([sysUp_m1_r, sysUp_m1_r_unc])
                
                sysUp_m1_g = sys_m1_g[0][0]
                sysUp_m1_g_unc = sys_m1_g[1][0]
                sysUp_m1_gen.append([sysUp_m1_g, sysUp_m1_g_unc])
                
                sysUp_m2_r = sys_m2_r[0][0]
                sysUp_m2_r_unc = sys_m2_r[1][0]
                sysUp_m2_rec.append([sysUp_m2_r, sysUp_m2_r_unc])
                
                sysUp_m2_g = sys_m2_g[0][0]
                sysUp_m2_g_unc = sys_m2_g[1][0]
                sysUp_m2_gen.append([sysUp_m2_g, sysUp_m2_g_unc])
                
                
                if args.sys != "TopPtReweight":
                    sysDn_m1_r = sys_m1_r[0][1]
                    sysDn_m1_r_unc = sys_m1_r[1][1]
                    sysDn_m1_rec.append([sysDn_m1_r, sysDn_m1_r_unc])
                    
                    sysDn_m1_g = sys_m1_g[0][1]
                    sysDn_m1_g_unc = sys_m1_g[1][1]
                    sysDn_m1_gen.append([sysDn_m1_g, sysDn_m1_g_unc])
                    
                    sysDn_m2_r = sys_m2_r[0][1]
                    sysDn_m2_r_unc = sys_m2_r[1][1]
                    sysDn_m2_rec.append([sysDn_m2_r, sysDn_m2_r_unc])
                    
                    sysDn_m2_g = sys_m2_g[0][1]
                    sysDn_m2_g_unc = sys_m2_g[1][1]
                    sysDn_m2_gen.append([sysDn_m2_g, sysDn_m2_g_unc])
                
                print "\nSystematic: %s" % args.sys 
                if args.sys == "TopPtReweight":        
                    print "Up rec: m1 = %f +- %f\tm2 = %f +- %f" % (sysUp_m1_r, sysUp_m1_r_unc, sysUp_m2_r, sysUp_m2_r_unc)
                    print "Up gen: m1 = %f +- %f\tm2 = %f +- %f" % (sysUp_m1_g, sysUp_m1_g_unc, sysUp_m2_g, sysUp_m2_g_unc)

                else:
                    print "Up rec: m1 = %f +- %f\tm2 = %f +- %f" % (sysUp_m1_r, sysUp_m1_r_unc, sysUp_m2_r, sysUp_m2_r_unc)
                    print "Up gen: m1 = %f +- %f\tm2 = %f +- %f" % (sysUp_m1_g, sysUp_m1_g_unc, sysUp_m2_g, sysUp_m2_g_unc)
                    print "Dn rec: m1 = %f +- %f\tm2 = %f +- %f" % (sysDn_m1_r, sysDn_m1_r_unc, sysDn_m2_r, sysDn_m2_r_unc)
                    print "Dn gen: m1 = %f +- %f\tm2 = %f +- %f" % (sysDn_m1_g, sysDn_m1_g_unc, sysDn_m2_g, sysDn_m2_g_unc)
            

        moments = {"obs":args.obs, "cut":args.cut, "nominal":{"m1":{"rec":m1_rec, "gen":m1_gen}, "m2":{"rec":m2_rec, "gen":m2_gen}} } 
        if args.sys != "":
            moments["sysUp"] = {"type":args.sys, "var":"Up", "m1":{"rec":sysUp_m1_rec, "gen":sysUp_m1_gen}, "m2":{"rec":sysUp_m2_rec, "gen":sysUp_m2_gen} }
            if args.sys != "TopPtReweight":
                moments["sysDown"] = {"type":args.sys, "var":"Down", "m1":{"rec":sysDn_m1_rec, "gen":sysDn_m1_gen}, "m2":{"rec":sysDn_m2_rec, "gen":sysDn_m2_gen} } 

        pickle.dump(moments, open("moments_%s_sys_%s_cut_%d.pkl" % (args.obs,args.sys,args.cut), "wb"))
    else:
        moments = pickle.load(open(args.pkl, "rb"))
        m1_rec = moments["nominal"]["m1"]["rec"]
        m1_gen = moments["nominal"]["m1"]["gen"]
        m2_rec = moments["nominal"]["m2"]["rec"]
        m2_gen = moments["nominal"]["m2"]["gen"]

    graphMoments(m1_rec, m1_gen, m2_rec, m2_gen, args.obs, MASSES) 
    

if __name__ == "__main__":
    main()
