import ROOT
from ROOT import TFile, TH1F, TH1D, TCanvas

class PyleupRW(object):
    def __init__(self, mc_file_list=None, pileupFile=None, PUweightHist=None):
	"""Initializes the pileup reweighter
	   Inputting mc_file_list and pileupFile calculates a new pileup weight histogram 
	   Inputting just PUweightHist creates a copy of the object 

	"""
	
	self.PUweightSum = 0  # sum of all of the pu corrections 
	self.events = 0  # sum of all the events which require pu corrections
	self.PUweightHist = None  # TH1D histogram
	self.mcPUHist = None
	ROOT.gROOT.cd()
	if mc_file_list is not None and pileupFile is not None and PUweightHist is not None:
	    print "Too many args. Either input mc_file_list and pileupFile OR PUweightHist"
	    return

	if mc_file_list is not None and pileupFile is not None:
	    # Create new pileup histogram
	    self._createPUweightHist(mc_file_list, pileupFile)

	elif PUweightHist is not None:
	    # Copy pileup histogram
	    self.PUweightHist = PUweightHist.Clone()
	    self.PUweightHist.SetDirectory(0)

    def _createPUweightHist(self, mc_file_list, pileupFile):
	# Internal method
	ROOT.gROOT.cd()
	puF = TFile.Open(pileupFile)
	self.PUweightHist = puF.Get("pileup")
	self.PUweightHist.SetDirectory(0)
	puF.Close()

	PUweightInt = self.PUweightHist.Integral()
	mcPU = None 
	for mc_file in mc_file_list:
	    #print "reading file ", mc_file
	    mcFile = TFile.Open(mc_file)
	    if not mcFile.Get("ggNtuplizer/hPUTrue"):
		print "no hPU histogram here!"
		PUweightHist = None
		return

	    if mcPU == None: 
		mcPU = mcFile.Get("ggNtuplizer/hPUTrue")
	    else: 
		mcPU.Add(mcFile.Get("ggNtuplizer/hPUTrue"))
	    
	    mcPU.SetDirectory(0)
	    mcFile.Close()

	self.mcPUHist = mcPU.Clone()
	self.mcPUHist.SetDirectory(0)

	mcPU.Scale(1.0/mcPU.Integral())
	self.PUweightHist.Divide(mcPU)
	self.PUweightHist.Scale(1.0/PUweightInt)


    def getWeight(self, nPUInfo, puBX, puTrue):
	PUweight = 0.0
	if self.PUweightHist is None:
	    print "PUweightHist invalid"
	    return 1.0

	for puInd in xrange(0, nPUInfo):
	    if puBX[puInd] == 0:
		PUweight = self.PUweightHist.GetBinContent(self.PUweightHist.GetXaxis().FindBin(puTrue[puInd]))
		break

	self.events += 1
	self.PUweightSum += PUweight
	return PUweight

    def getAvgWeight(self):
	return -1.0 if self.events == 0 else self.PUweightSum/self.events 

