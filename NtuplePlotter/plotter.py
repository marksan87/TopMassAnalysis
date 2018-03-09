#!/usr/bin/env python

import optparse
import os,sys
import json
import ROOT
import math

from ROOT import kBlue
# Dimensions of canvas
_canvas_width = 1000
_canvas_height = 1000

useGrid = False


_plottypes = {} #"bjet_eta":"Bjet #eta", 
	  #  "bjet_mult":"Bjet Multiplicity",
	  #  "bjet_pt":"Bjet p_{T}",
	  #  "ele_eta":"Electron #void8 #eta #void8",
	  #  "ele_sc_eta":"Electron #void8 #eta_{SuperCluster} #void8",
	  #  "ele_pt":"Electron p_{T}",
	  #  "ele_eta_signed":"Electron #eta",
	  #  "ele_sc_eta_signed":"Electron #eta_{SuperCluster}",
	  #  "Ep_Em":"E(l^{+}) + E(l^{-})",
	  #  "jet_eta":"Jet #void8 #eta #void8",
	  #  "jet_mult":"Jet multiplicity",
	  #  "jet_pt":"Jet p_{T}",
	  #  "mu_eta":"Muon #void8 #eta #void8",
	  #  "mu_eta_signed":"Muon #eta",
	  #  "mu_pt":"Muon p_{T}"
	  #  }

#class TheFooBar:    
#    def __init(self, val):
#	self.value = val
#    def doThis(self, num):
#	print "num * val = %s" % (num * val)
"""
A wrapper to store data and MC histograms for comparison
"""
class Plot(object):

    def __init__(self,name):
        self.name = name
        self.mc = {}
        self.dataH = None
        self.data = None
	self.totMC = None
	self._garbageList = []
        #self.plotformats = ['pdf','png']
        self.plotformats = ['png']
	self.savelog = False
        #self.ratiorange = (0.46,1.54)
        self.ratiorange = (0.7,1.3)


    def add(self, h, title, color, isData):
        h.SetTitle(title)
        if isData:
            try:
                self.dataH.Add(h)
            except:
                self.dataH=h
                self.dataH.SetDirectory(0)
                self.dataH.SetMarkerStyle(20)
                self.dataH.SetMarkerSize(1.4)
                self.dataH.SetMarkerColor(color)
                self.dataH.SetLineColor(ROOT.kBlack)
                self.dataH.SetLineWidth(2)
                self.dataH.SetFillColor(0)
                self.dataH.SetFillStyle(0)
                self._garbageList.append(h)
        else:
            try:
                self.mc[title].Add(h)
            except:
                self.mc[title]=h
                self.mc[title].SetName('%s_%s' % (self.mc[title].GetName(), title ) )
                self.mc[title].SetDirectory(0)
                self.mc[title].SetMarkerStyle(1)
                self.mc[title].SetMarkerColor(color)
                self.mc[title].SetLineColor(ROOT.kBlack)
                self.mc[title].SetLineWidth(1)
                self.mc[title].SetFillColor(color)
                self.mc[title].SetFillStyle(1001)
                self._garbageList.append(h)

    def finalize(self):
        self.data = convertToPoissonErrorGr(self.dataH)

    # Writes histograms to plotter.root
    def appendTo(self,outUrl):
        outF = ROOT.TFile.Open(outUrl,'UPDATE')
        if not outF.cd(self.name):
            outDir = outF.mkdir(self.name)
            outDir.cd()
	if self.totMC is not None:
	    self.totMC.Write(self.totMC.GetName(), ROOT.TObject.kOverwrite)
        for m in self.mc :
            self.mc[m].Write(self.mc[m].GetName(), ROOT.TObject.kOverwrite)
        if self.dataH :
            self.dataH.Write(self.dataH.GetName(), ROOT.TObject.kOverwrite)
        if self.data :
            self.data.Write(self.data.GetName(), ROOT.TObject.kOverwrite)
        outF.Close()

    def reset(self):
        for o in self._garbageList:
            try:
                o.Delete()
            except:
                pass

    def show(self, outDir,lumi,title="",noScale=False,saveTeX=False):

        if len(self.mc)==0:
            print '%s has no MC!' % self.name
            #return

        elif self.mc.values()[0].InheritsFrom('TH2') :
            print 'Skipping TH2'
            #return

        c = ROOT.TCanvas('c','c',_canvas_width, _canvas_height)
        c.SetBottomMargin(0.0)
        c.SetLeftMargin(0.0)
        c.SetTopMargin(0)
        c.SetRightMargin(0.00)

        #holds the main plot
        c.cd()
        p1 = ROOT.TPad('p1','p1',0.0,0.95,1.0,0.15)
        p1.Draw()
        p1.SetRightMargin(0.05)
        p1.SetLeftMargin(0.12)
        p1.SetTopMargin(0.01)
        p1.SetBottomMargin(0.12)
        p1.SetGridx(useGrid)
	self._garbageList.append(p1)
        p1.cd()

        # legend
        leg = ROOT.TLegend(0.45, 0.875-0.02*max(len(self.mc)-2,0), 0.98, 0.925)        
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(43)
        leg.SetTextSize(16)
        nlegCols = 0

        if self.dataH is not None:
            if self.data is None: self.finalize()
            leg.AddEntry( self.data, self.data.GetTitle(),'p')
            nlegCols += 1
        for h in self.mc:
            if not noScale : self.mc[h].Scale(lumi)
            leg.AddEntry(self.mc[h], self.mc[h].GetTitle(), 'f')
            nlegCols += 1
        if nlegCols ==0 :
            print '%s is empty'%self.name
            return
        leg.SetNColumns(ROOT.TMath.Min(nlegCols/2,3))

        # Build the stack to plot from all backgrounds
        totalMC = None
        stack = ROOT.THStack('mc','mc')
        for h in self.mc:
            stack.Add(self.mc[h],'hist')
            try:
                totalMC.Add(self.mc[h])
            except:
                totalMC = self.mc[h].Clone('totalmc')
                self._garbageList.append(totalMC)
                totalMC.SetDirectory(0)
	self.totMC = totalMC
	self.totMC.name = "totalMC"
	self.totMC.title = "MC"
    
	#print "about to create frame"
        frame = totalMC.Clone('frame') if totalMC is not None else self.dataH.Clone('frame')
        frame.Reset('ICE')
	maxY = 0
        if totalMC:
            maxY = totalMC.GetMaximum() 
        if self.dataH:
            if maxY<self.dataH.GetMaximum():
                maxY=self.dataH.GetMaximum()
        frame.GetYaxis().SetRangeUser(0.1,maxY*1.3)
        frame.SetDirectory(0)
        frame.Reset('ICE')
        self._garbageList.append(frame)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetLabelSize(0.04)
        frame.GetYaxis().SetNoExponent()

	if title in _plottypes.keys():
	    frameTitle = _plottypes[title]
	else:
	    print "Something went wrong :/"
	    frameTitle = title
	frame.SetTitle(frameTitle)
        frame.Draw()
        frame.GetYaxis().SetTitleOffset(1.3)


	# Draw histograms
        if totalMC is not None: 
	    stack.Draw('hist same')
	    # Draw error regions
	    err = totalMC.Clone()
	    err.SetFillColor(kBlue)
	    err.SetFillStyle(3018)
	    err.Draw("e2same")

        if self.data is not None : self.data.Draw('p')



        leg.Draw()
        txt=ROOT.TLatex()
        txt.SetNDC(True)
        txt.SetTextFont(43)
        txt.SetTextSize(20)
        txt.SetTextAlign(12)
        if lumi<100:
            txt.DrawLatex(0.18,0.92,'#bf{CMS} #it{Preliminary} %3.1f pb^{-1} (13 TeV)' % (lumi) )
        else:
            txt.DrawLatex(0.18,0.92,'#bf{CMS} #it{Preliminary} %3.1f fb^{-1} (13 TeV)' % (lumi/1000.) )

        #holds the ratio
        c.cd()
        #p2 = ROOT.TPad('p2','p2',0.0,0.85,1.0,1.0) 
        p2 = ROOT.TPad('p2','p2',0.0,0.02,1.0,0.17)
	p2.Draw()
        p2.SetBottomMargin(0.01)
        p2.SetRightMargin(0.05)
        p2.SetLeftMargin(0.12)
        p2.SetTopMargin(0.05)
        p2.SetGridx(useGrid)
        p2.SetGridy(True)
        #p2.SetGridy(useGrid)
        self._garbageList.append(p2)
        p2.cd()
        ratioframe=frame.Clone('ratioframe')
	ratioframe.GetYaxis().SetTitle('Data/MC')
        ratioframe.GetYaxis().SetRangeUser(self.ratiorange[0], self.ratiorange[1])
        self._garbageList.append(frame)
        ratioframe.GetYaxis().SetNdivisions(5)
        ratioframe.GetYaxis().SetLabelSize(0.18)        
        ratioframe.GetYaxis().SetTitleSize(0.2)
        ratioframe.GetYaxis().SetTitleOffset(0.2)
        ratioframe.GetXaxis().SetLabelSize(0)
        ratioframe.GetXaxis().SetTitleSize(0)
        ratioframe.GetXaxis().SetTitleOffset(0)
        ratioframe.Draw()

        try:
            ratio=self.dataH.Clone('ratio')
            ratio.SetDirectory(0)
            self._garbageList.append(ratio)
            ratio.Divide(totalMC)
            gr=ROOT.TGraphAsymmErrors(ratio)
            gr.SetMarkerStyle(self.data.GetMarkerStyle())
            gr.SetMarkerSize(self.data.GetMarkerSize())
            gr.SetMarkerColor(self.data.GetMarkerColor())
            gr.SetLineColor(self.data.GetLineColor())
            gr.SetLineWidth(self.data.GetLineWidth())
	    #gr.SetOptStat(0)
            gr.Draw('p')
	    ratioErr = gr.Clone()
	    ratioErr.SetFillColor(kBlue)
	    ratioErr.SetFillStyle(3018)
	    ratioErr.Draw("e2same")
        except:
            pass

        #all done
        c.cd()
	c.Modified()
        c.Update()
        #save
        for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'.'+ext))
        if self.savelog:
            p1.cd()
            p1.SetLogy()
            c.cd()
            c.Modified()
            c.Update()
            for ext in self.plotformats : c.SaveAs(os.path.join(outDir, self.name+'_log.'+ext))

        if saveTeX : self.convertToTeX(outDir=outDir)


    def convertToTeX(self, outDir):
        if len(self.mc)==0:
            print '%s is empty' % self.name
            return

        f = open(outDir+'/'+self.name+'.dat','w')
        f.write('------------------------------------------\n')
        f.write("Process".ljust(20),)
        f.write("Events after each cut\n")
        f.write('------------------------------------------\n')

        tot ={}
        err = {}
        f.write(' '.ljust(20),)
        try:
            for xbin in xrange(1,self.mc.values()[0].GetXaxis().GetNbins()+1):
                pcut=self.mc.values()[0].GetXaxis().GetBinLabel(xbin)
                f.write(pcut.ljust(40),)
                tot[xbin]=0
                err[xbin]=0
        except:
            pass
        f.write('\n')
        f.write('------------------------------------------\n')

        for pname in self.mc:
            h = self.mc[pname]
            f.write(pname.ljust(20),)

            for xbin in xrange(1,h.GetXaxis().GetNbins()+1):
                itot=h.GetBinContent(xbin)
                ierr=h.GetBinError(xbin)
                pval=' & %3.1f $\\pm$ %3.1f' % (itot,ierr)
                f.write(pval.ljust(40),)
                tot[xbin] = tot[xbin]+itot
                err[xbin] = err[xbin]+ierr*ierr
            f.write('\n')

        f.write('------------------------------------------\n')
        f.write('Total'.ljust(20),)
        for xbin in tot:
            pval=' & %3.1f $\\pm$ %3.1f' % (tot[xbin],math.sqrt(err[xbin]))
            f.write(pval.ljust(40),)
        f.write('\n')

        if self.dataH is None: return
        f.write('------------------------------------------\n')
        f.write('Data'.ljust(20),)
        for xbin in xrange(1,self.dataH.GetXaxis().GetNbins()+1):
            itot=self.dataH.GetBinContent(xbin)
            pval=' & %d'%itot
            f.write(pval.ljust(40))
        f.write('\n')
        f.write('------------------------------------------\n')
        f.close()



"""
converts a histogram to a graph with Poisson error bars
"""
def convertToPoissonErrorGr(h):

    htype=h.ClassName()
    if htype.find('TH1')<0 : return None

    #check https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars
    alpha = 1 - 0.6827;
    grpois = ROOT.TGraphAsymmErrors(h);
    for i in xrange(0,grpois.GetN()+1) :
        N = grpois.GetY()[i]
        if N<200 :
            L = 0
            if N>0 : L = ROOT.Math.gamma_quantile(alpha/2,N,1.)
            U = ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
            grpois.SetPointEYlow(i, N-L)
            grpois.SetPointEYhigh(i, U-N)
        else:
            grpois.SetPointEYlow(i, math.sqrt(N))
            grpois.SetPointEYhigh(i,math.sqrt(N))
    return grpois


"""
steer the script
"""
def main():

    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-j', '--json',        dest='json'  ,      help='json with list of files',        default=None,    type='string')
    parser.add_option('-i', '--inDir',       dest='inDir' ,      help='input directory',                default=None,    type='string')
    parser.add_option(      '--saveLog',     dest='saveLog' ,    help='save log versions of the plots', default=False,   action='store_true')
    parser.add_option(      '--silent',      dest='silent' ,     help='only dump to ROOT file',         default=False,   action='store_true')
    parser.add_option(      '--saveTeX',     dest='saveTeX' ,    help='save as tex file as well',       default=False,   action='store_true')
    parser.add_option(      '--rebin',       dest='rebin',       help='rebin factor',                   default=1,       type=int)
    parser.add_option('-l', '--lumi',        dest='lumi' ,       help='lumi to print out',              default=41.6,    type=float)
    parser.add_option(      '--only',        dest='only',        help='plot only these (csv)',          default='',      type='string')
    (opt, args) = parser.parse_args()

    #read list of samples
    jsonFile = open(opt.json,'r')
    samplesList=json.load(jsonFile,encoding='utf-8').items()
    jsonFile.close()

    onlyList=opt.only.split(',')

    #read plots 
    plots={}
    for tag,sample in samplesList: 
        fIn=ROOT.TFile.Open('%s/%s.root' % ( opt.inDir, tag) )
	print 'opening %s/%s.root' % ( opt.inDir, tag)
	#print tag
	#print sample
        try:
            for tkey in fIn.GetListOfKeys():
                key=tkey.GetName()
                keep=False
                for tag in onlyList: 
                    if tag in key: keep=True
                if not keep: continue
                obj=fIn.Get(key)
                if not obj.InheritsFrom('TH1') : continue
                if not key in plots : plots[key]=Plot(key)
                if opt.rebin>1:  obj.Rebin(opt.rebin)
		#print "plot %s  Title %s " %(key, obj.GetTitle())
		_plottypes.update( {key:obj.GetTitle()} )	
                plots[key].add(h=obj,title=sample[3],color=sample[4],isData=sample[1])
               # plots[key].add(h=obj,title=sample[3],color=sample[4],isData=sample[1])
        except:
            print 'Skipping %s'%tag

    #show plots
    #ROOT.gStyle.SetOptTitle(0)
    #ROOT.gStyle.SetOptStat(1111)
    ROOT.gStyle.SetOptTitle(1)
    ROOT.gStyle.SetOptStat(0)
    #ROOT.gStyle.SetOptStat("eimr")

    ROOT.gROOT.SetBatch(True)
    outDir=opt.inDir+'/plots'
    os.system('mkdir -p %s' % outDir)
    #print plots
    for p in plots : 
        try:
	    if opt.saveLog    : plots[p].savelog=True
	    
	    ######################################################################################
	    # if not opt.silent : plots[p].show(outDir=outDir,lumi=opt.lumi,saveTeX=opt.saveTeX)
	    if not opt.silent : plots[p].show(outDir=outDir,lumi=opt.lumi,title=p, noScale=True, saveTeX=opt.saveTeX)
	    ###################################################################################################
	    #plots[p].SetTitle(p)
	    #print p
	    plots[p].appendTo(outDir+'/plotter.root')
	    plots[p].reset()
	except:
	    print "Error plotting %s" % p
	    continue

    print '-'*50
    print 'Plots and summary ROOT file can be found in %s' % outDir
    print '-'*50


		
        
"""
for execution from another script
"""
if __name__ == "__main__":
    sys.exit(main())

