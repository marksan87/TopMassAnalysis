#!/usr/bin/env python
from ROOT import *
from numpy import mean,std
from array import array
import os

mt = [166.5, 169.5, 171.5, 172.5, 173.5, 175.5, 178.5]
#mt = [166.5,172.5]
obsTitle = {"ptll":"p_{T}(ll)", "ptpos":"p_{T}(l^{+})", "Epos":"E(l^{+})", "ptp_ptm":"p_{T}(l^{+}) + p_{T}(l^{-})", "Ep_Em":"E(l^{+}) + E(l^{-})", "Mll":"M(ll)"}
nominalMoments = {166.5:{"m1":{"mean":76.3576, "rms":0.124111}, "m2":{"mean":6077.0495677691215,"rms":15.602755728226905}}, 169.5:{"m1":{"mean":77.1106, "rms":0.0708639}, "m2":{"mean":6185.08427132322, "rms":16.13228088365606}}, 171.5:{"m1":{"mean":77.472691, "rms":0.123540}, "m2":{"mean":6249.488443324806, "rms":16.601225302314273}}, 172.5:{"m1":{"mean":77.7107, "rms":0.0613487}, "m2":{"mean":6280.077593464887, "rms":16.75315227955084}}, 173.5:{"m1":{"mean":78.0883, "rms":0.12344}, "m2":{"mean":6347.766431941328, "rms":17.083351544338726}}, 175.5:{"m1":{"mean":78.4646, "rms":0.0697152}, "m2":{"mean":6409.581483861747, "rms":17.49296794295303}}, 178.5:{"m1":{"mean":78.9815, "rms":0.131812}, "m2":{"mean":6502.114447920372, "rms":18.22841162550118}}}
#nominalMoments = {166.5:{"m1":{"mean":69.66342415215317, "rms":0.0951962650084965}, "m2":{"mean":6077.0495677691215,"rms":15.602755728226905}}, 169.5:{"m1":{"mean":70.41404068664811, "rms":0.09796714000046931}, "m2":{"mean":6185.08427132322, "rms":16.13228088365606}}, 171.5:{"m1":{"mean":70.76569118944157, "rms":0.1004355771116041}, "m2":{"mean":6249.488443324806, "rms":16.601225302314273}}, 172.5:{"m1":{"mean":70.96403812965019, "rms":0.10125787141595022}, "m2":{"mean":6280.077593464887, "rms":16.75315227955084}}, 173.5:{"m1":{"mean":71.35479828694046, "rms":0.10280758504026101}, "m2":{"mean":6347.766431941328, "rms":17.083351544338726}}, 175.5:{"m1":{"mean":71.72650337451793, "rms":0.1049925443875296}, "m2":{"mean":6409.581483861747, "rms":17.49296794295303}}, 178.5:{"m1":{"mean":72.26451810322939, "rms":0.10866138114513721}, "m2":{"mean":6502.114447920372, "rms":18.22841162550118}}}


obs = "ptll"
#inDir = "Ctoys_new"
inDir = "pois_mt"
outDir = "%s/%s_plots" % (inDir,obs)
os.system("mkdir -p %s" % outDir)
moments = {}
for m in mt:
    with open("%s%d/rec_ptll_mt%d.txt" % (inDir,10*m, 10*m), "r") as f:
        for i,line in enumerate(f):
            exec("_m%d = %s" % (i+1,line))

    moments[m] = {"m1":{"toys":_m1, "mean":mean(_m1), "rms":std(_m1)} , "m2":{"toys":_m2, "mean":mean(_m2), "rms":std(_m2)}}
gROOT.SetBatch(True)
def graphMoments(moments, obs, masses, outDir):
    m1 = []
    m1_unc = []
    m2 = []
    m2_unc = []
    for m in masses:
        m1.append(moments[m]["m1"]["mean"])
        m1_unc.append(moments[m]["m1"]["rms"])
        m2.append(moments[m]["m2"]["mean"])
        m2_unc.append(moments[m]["m2"]["rms"])

    m1G = TGraphErrors(len(m1), array('d', masses), array('d', m1), array('d', [0.]*len(m1)), array('d', m1_unc))
    m2G = TGraphErrors(len(m2), array('d', masses), array('d', m2), array('d', [0.]*len(m2)), array('d', m2_unc))

    m1G.GetXaxis().SetTitle("m_{t} [GeV]")
    m1G.GetYaxis().SetTitle("O^{1} %s [GeV]" % obsTitle[obs])
    m1G.GetYaxis().SetTitleOffset(1.2)
    
    m2G.GetXaxis().SetTitle("m_{t} [GeV]")
    m2G.GetYaxis().SetTitle("O^{2} %s [GeV]" % obsTitle[obs])
    m2G.GetYaxis().SetTitleOffset(1.2)
    
    #gStyle.SetMarkerColor(kBlue)
    gStyle.SetLineColor(kBlack)
    #gStyle.SetMarkerStyle(22)
    #gStyle.SetMarkerSize(4.0)
    m1G.SetMarkerStyle(22)
    m1G.SetMarkerColor(kBlue)
    m2G.SetMarkerStyle(22)
    m2G.SetMarkerColor(kBlue)

    #m1G.SetMarkerSize(1.0)
    #m1G.SetMarkerSize(2.0)
    #m2G.SetMarkerSize(2.0)
    
    m1G.SetTitle("Moment 1  %s rec" % obsTitle[obs])
    m1G.SetName("m1_rec_%s" % obs)
    m2G.SetTitle("Moment 2  %s rec" % obsTitle[obs])
    m2G.SetName("m2_rec_%s" % obs)

    m1_histos = {}
    m2_histos = {}
    m1_residuals = {}
    m2_residuals = {}

    m1_reslist = []
    m2_reslist = []
    m1err_reslist = []
    m2err_reslist = []
    for i,m in enumerate(masses):
        m1toys = moments[m]["m1"]["toys"]
        m2toys = moments[m]["m2"]["toys"]
        m1h = TH1D("m1_mt%d_%s" % (10*m, obs), "Moment 1 Toys  %s rec  m_{T} = %.1f" % (obsTitle[obs], m), 50, 0.99*min(m1toys), 1.01*max(m1toys))
        m2h = TH1D("m2_mt%d_%s" % (10*m, obs), "Moment 2 Toys  %s rec  m_{T} = %.1f" % (obsTitle[obs], m), 50, 0.99 * min(m2toys), 1.01 * max(m2toys))
        
        # Residuals
        m1res = TH1D("Residual_m1_mt%d_%s" % (10*m, obs), "Moment 1 Bias  %s rec  m_{T} = %.1f" % (obsTitle[obs], m), 50, -5., 5.)
        m2res = TH1D("Residual_m2_mt%d_%s" % (10*m, obs), "Moment 2 Bias  %s rec  m_{T} = %.1f" % (obsTitle[obs], m), 50, -5., 5.)
        
        m1res.GetXaxis().SetTitle("O^{1} Bias")
        m1res.GetYaxis().SetTitle("Toys")
        m2res.GetXaxis().SetTitle("O^{2} Bias")
        m2res.GetYaxis().SetTitle("Toys")
        
        m1h.GetXaxis().SetTitle("O^{1} %s [GeV]" % obsTitle[obs])
        m1h.GetYaxis().SetTitle("Toys")
        m2h.GetXaxis().SetTitle("O^{2} %s [GeV^{2}]" % obsTitle[obs])
        m2h.GetYaxis().SetTitle("Toys")
        
        for m1 in m1toys:
            m1h.Fill(m1)
            m1res.Fill((m1 - nominalMoments[m]["m1"]["mean"]) / nominalMoments[m]["m1"]["rms"])
        for m2 in m2toys:
            m2h.Fill(m2)
            m2res.Fill((m2 - nominalMoments[m]["m2"]["mean"]) / nominalMoments[m]["m2"]["rms"])
       
        m1_histos[m] = m1h
        m2_histos[m] = m2h
        

        m1_reslist.append(m1res.GetMean())
        m1err_reslist.append(m1res.GetMeanError())
        m2_reslist.append(m2res.GetRMS())
        m2_reslist.append(m2res.GetRMSError())

        m1_residuals[m] = m1res
        m2_residuals[m] = m2res

    m1resG = TGraphErrors(len(m1_reslist), array('d', masses), array('d', m1_reslist), array('d', [0.]*len(m1_reslist)), array('d', m1err_reslist))
    #m2resG = TGraphErrors(len(m2_reslist), array('d', masses), array('d', m2_reslist), array('d', [0.]*len(m2)), array('d', m2_unc))

    m1resG.SetTitle("%s Moment 1 Bias" % obsTitle[obs])
    m1resG.GetXaxis().SetTitle("m_{t} [GeV]")
    m1resG.GetYaxis().SetTitle("O^{1} %s Bias" % obsTitle[obs])
    m1resG.GetYaxis().SetTitleOffset(1.2)
    
    #m2resG.SetTitle("Moment 2 Residuals")
    #m2resG.GetXaxis().SetTitle("m_{t} [GeV]")
    #m2resG.GetYaxis().SetTitle("O^{2} %s [GeV]" % obsTitle[obs])
    #m2resG.GetYaxis().SetTitleOffset(1.2)
    
    c = TCanvas('c','c', 1200, 800)
    gStyle.SetTitleFontSize(0.04)
    #c.SetLeftMargin(0.15);
    c.SetRightMargin(0.15)
    #c.SetBottomMargin(0.25);
    #pad1=TPad('p1','p1',0.05,0.05,0.95,0.95)
    pad1=TPad('p1','p1',0.,0.,1.,0.97)
    pad1.Draw()
    
    outF = TFile.Open("%s/%s_toyMomentPlots.root" % (outDir, obs), "RECREATE")
    m1G.Fit("pol1") 
    f1 = m1G.GetFunction("pol1")
    p0 = f1.GetParameter(0)
    p0_err = f1.GetParError(0)
    p1 = f1.GetParameter(1)
    p1_err = f1.GetParError(1)
    fitline1 = "offset %.f #pm %.f   slope %.3f #pm %.2f" % (p0, p0_err, p1, p1_err)

    pad1.cd()
    m1G.Draw("AP")
    txt=TLatex()
    txt.SetNDC(True)
    txt.SetTextFont(43)
    txt.SetTextSize(20)
    txt.SetTextAlign(12)
    txt.DrawLatex(0.1,0.92,'#bf{CMS} #it{Work in Progress}  %3.1f fb^{-1} (13 TeV)' % (35.9) )
    txt.DrawLatex(0.55,0.92, fitline1)
    m1G.Write()
    c.SaveAs("%s/moment1_rec_%s.png" % (outDir,obs))


    m2G.Fit("pol1")
    f2 = m2G.GetFunction("pol1")
    p0 = f2.GetParameter(0)
    p0_err = f2.GetParError(0)
    p1 = f2.GetParameter(1)
    p1_err = f2.GetParError(1)
    fitline2 = "offset %.f #pm %.f   slope %.3f #pm %.2f" % (p0, p0_err, p1, p1_err)

    #pad1.cd()
    m2G.Draw("AP")
    txt=TLatex()
    txt.SetNDC(True)
    txt.SetTextFont(43)
    txt.SetTextSize(20)
    txt.SetTextAlign(12)
    txt.DrawLatex(0.1,0.92,'#bf{CMS} #it{Work in Progress}  %3.1f fb^{-1} (13 TeV)' % (35.9) )
    txt.DrawLatex(0.55,0.92, fitline2)
    m2G.Write()
    c.SaveAs("%s/moment2_rec_%s.png" % (outDir,obs))

    m1resG.Fit("pol1")
    f2 = m1resG.GetFunction("pol1")
    p0 = f2.GetParameter(0)
    p0_err = f2.GetParError(0)
    p1 = f2.GetParameter(1)
    p1_err = f2.GetParError(1)
    fitline2 = "offset %.f #pm %.f   slope %.3f #pm %.2f" % (p0, p0_err, p1, p1_err)
    m1resG.Draw("AP")
    txt=TLatex()
    txt.SetNDC(True)
    txt.SetTextFont(43)
    txt.SetTextSize(20)
    txt.SetTextAlign(12)
    txt.DrawLatex(0.1,0.92,'#bf{CMS} #it{Work in Progress}  %3.1f fb^{-1} (13 TeV)' % (35.9) )
    txt.DrawLatex(0.55,0.92, fitline2)
    m1resG.Write()
    c.SaveAs("%s/bias_moment1_rec_%s.png" % (outDir,obs))
    """
    m2resG.Fit("pol1")
    f2 = m2resG.GetFunction("pol1")
    p0 = f2.GetParameter(0)
    p0_err = f2.GetParError(0)
    p1 = f2.GetParameter(1)
    p1_err = f2.GetParError(1)
    fitline2 = "offset %.f #pm %.f   slope %.3f #pm %.2f" % (p0, p0_err, p1, p1_err)
    m2resG.Draw("AP")
    txt=TLatex()
    txt.SetNDC(True)
    txt.SetTextFont(43)
    txt.SetTextSize(20)
    txt.SetTextAlign(12)
    txt.DrawLatex(0.1,0.92,'#bf{CMS} #it{Work in Progress}  %3.1f fb^{-1} (13 TeV)' % (35.9) )
    txt.DrawLatex(0.55,0.92, fitline2)
    m2resG.Write()
    c.SaveAs("%s/res_moment2_rec_%s.png" % (outDir,obs))
    """
    for m in masses:
        m1_histos[m].Draw("HIST")
        m1_histos[m].Write()
        c.SaveAs("%s/m1_mt%d.png" % (outDir,10*m))
        m2_histos[m].Draw("HIST")
        m2_histos[m].Write()
        c.SaveAs("%s/m2_mt%d.png" % (outDir,10*m))

        m1_residuals[m].Draw("HIST")
        m1_residuals[m].Write()
        c.SaveAs("%s/res_m1_mt%d.png" % (outDir,10*m))
        m2_residuals[m].Draw("HIST")
        m2_residuals[m].Write()
        c.SaveAs("%s/res_m2_mt%d.png" % (outDir,10*m))
    
    #m1G.Draw("AP")
    #m1G.Write()
    #m2G.Draw("AP")
    #m2G.Write()
    #for m in masses:
    #    m1_histos[m].Write()
    #    m2_histos[m].Write()
    #outF.Write()
    outF.Close()


graphMoments(moments, obs, mt, outDir)

