#!/usr/bin/env python

from ROOT import *
#from toyMoments import createToyMoments
from toys_C import createToyMoments
import os

f = TFile.Open("ttrees/tt/mc_TT.root")
t = f.Get("goodEvents")
masses = ['166_5', '169_5', '171_5', '172_5', '173_5', '175_5', '178_5']

for m in masses:
    if m != '172_5':
        exec("f_%s = TFile.Open('ttrees/tt/mc_TT-mt%s.root')" % (m[:-2], m.replace('_','')))
        exec("t_%s = f.Get('goodEvents')" % m[:-2])


gROOT.SetBatch(True)
os.system("mkdir -p toyMoments")
outF = TFile.Open("toyMoments/toyMoments.root", "recreate")
MASSES = [166.5, 169.5, 171.5, 172.5, 173.5, 175.5, 178.5]

def graphMoments(m1, m2, obs, masses = MASSES):
    outDir = "unbinnedMoments/%s" % obs
    os.system("mkdir -p %s" % outDir)
    print "====================="
    print "Moments"

    m1G = TGraphErrors(len(masses), masses, m1[0], 0., m1[1])
    m2G = TGraphErrors(len(masses), masses, m2[0], 0., m2[1])
    gStyle.SetMarkerColor(kBlue)
    gStyle.SetLineColor(kBlack)



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



print "Creating toys"
cut = 180
npoints = 1000
ntoys = 10
for m in masses:
    if m != '172_5':
        print "mt = %s" % m.replace('_','.')
        exec("mt%s_m1toys,mt%s_m2toys,mt%s_moment1,mt%s_moment2 = createToyMoments(t, 'ptll', cut, npoints, ntoys, '%s')" % (m[:-2], m[:-2], m[:-2], m[:-2], m))
    else:
        print "mt = 172.5"
        m1toys,m2toys, moment1, moment2 = createToyMoments(t, "ptll", cut, npoints, ntoys,'172_5')


m1toys.Draw("hist")
from ROOT import c1 as c
c.SaveAs("toyMoments/mt172_5-moment1.png")

m2toys.Draw("hist")
c.SaveAs("toyMoments/mt172_5-moment2.png")

for m in masses:
    if m != '172_5':
        exec("mt%s_m1toys.Draw('hist')" % m[:-2])
        exec("c.SaveAs('toyMoments/mt%s-moment1.png')" % m)
        exec("mt%s_m2toys.Draw('hist')" % m[:-2])
        exec("c.SaveAs('toyMoments/mt%s-moment2.png')" % m)
